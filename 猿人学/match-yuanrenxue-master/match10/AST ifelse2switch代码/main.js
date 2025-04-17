const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types")
const generator = require("@babel/generator").default;
const fs = require("fs");

// npm install @babel/core 安装依赖
var jscode = fs.readFileSync('eval.js').toString()

const ast = parser.parse(jscode);


function step1(ast) {
  traverse(ast, {
    IfStatement: replaceifstate2block
  })
  traverse(ast, {
    ExpressionStatement: addblockwrap
  })
  function replaceifstate2block(path) {
    // 对alternate是IfStatement套一个blockStatement
    let alternate_path = path.get('alternate');
    let node = alternate_path.node;
    if (!t.isIfStatement(node)) return;
    alternate_path.replaceWith(t.blockStatement([node]))
  }
  function addblockwrap(path) {
    let node = path.node;
    let parentNode = path.parent;
    // 当前节点的父节点也是IfStatement的情况
    if (t.isIfStatement(parentNode)) {
      path.replaceWith(t.blockStatement([node]));
    }
  }
}
// 将if...else if...else语句转为if...else语句  给没有括号的if...else语句加上括号
step1(ast);

function replaceWhile(path) {
  // 反控制流平坦化    
  var node = path.node;
  // 判断是否是目标节点   
  if (!(t.isBooleanLiteral(node.test) || t.isUnaryExpression(node.test) || t.isLiteral(node.test)))
    // 如果while中不为true或!![]
    return;
  if (!(node.test.prefix || node.test.value))
    // 如果while中的值不为true
    return;
  var body = node.body.body;
  // var body = node.body;
  // console.log(t.isBlockStatement(body))
  if (!t.isIfStatement(body[1]))
    return;
  var ifstat = body[1];
  var caseList = [];
  solveIfStat(ifstat)

  function solveIfStat(ifstat) {
    if (t.isBinaryExpression(ifstat.test)){
      var consequentstat = ifstat.consequent;
      var alternatestat = ifstat.alternate;
      solveConsequentStat(consequentstat);
      solveAlternateStat(alternatestat);
    }else{
      //其他非控制流的if表达式
      caseList.push(ifstat)
    }
    
  }
  function solveConsequentStat(consequentstat) {
    if (!t.isBlockStatement(consequentstat)) return
    if (t.isIfStatement(consequentstat.body[0])) {
      solveIfStat(consequentstat.body[0])
    } else {
      // 对于consequentstat.body 只有一个元素的把外面的括号拆了
      if (consequentstat.body.length == 1){
        caseList.push(consequentstat.body[0]);
      }else{
        caseList.push(consequentstat);
      }
    }
  }
  function solveAlternateStat(alternatestat) {
    if (!t.isBlockStatement(alternatestat)) return
    if (t.isIfStatement(alternatestat.body[0])) {
      solveIfStat(alternatestat.body[0])
    } else {
      if (alternatestat.body.length == 1){
        caseList.push(alternatestat.body[0]);
      }else{
        caseList.push(alternatestat);
      }
    }
  }
  // console.log(caseList)
  console.log(caseList.length)
  // 自增表达式
	let discriminNode = body[0].expression;
  for (let index = 0; index < caseList.length; index++) {
    let testNode = t.valueToNode(index);
    let consequent = [caseList[index], t.breakStatement()];
    let SwitchCaseNode = t.SwitchCase(testNode, consequent);
    caseList[index] = SwitchCaseNode;
  }
  let switchNode = t.SwitchStatement(discriminNode, caseList);
  path.get('body.body')[1].replaceWith(switchNode)
  path.get('body.body')[0].remove()
}
traverse(ast, { WhileStatement: { exit: [replaceWhile] }, })


var code = generator(ast)['code']
console.log(code)
fs.writeFileSync('eval-switch.js',code)


