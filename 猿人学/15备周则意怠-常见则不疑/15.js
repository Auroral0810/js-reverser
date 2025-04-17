const fs = require('fs');
let wasmInstance = null;

// 同步加载WebAssembly
try {
  const wasmBuffer = fs.readFileSync('encode.wasm');
  const wasmModule = new WebAssembly.Module(wasmBuffer);
  wasmInstance = new WebAssembly.Instance(wasmModule);
  // console.log("WebAssembly loaded successfully");
} catch (error) {
  // console.error("Failed to load WebAssembly:", error);
}

// 同步获取签名
function getSignatureSync() {
  if (!wasmInstance) {
    throw new Error("WebAssembly not loaded");
  }
  
  const q = wasmInstance.exports.encode;
  const t1 = parseInt(Date.parse(new Date())/1000/2);
  const t2 = parseInt(Date.parse(new Date())/1000/2 - Math.floor(Math.random() * (50) + 1));
  return q(t1, t2).toString() + '|' + t1 + '|' + t2;
}

// 导出签名
// module.exports = getSignatureSync();
// 同时在控制台输出，便于调试
// console.log("Signature:", module.exports);
