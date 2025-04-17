var list = {
    "page": window.page,
    "m": btoa('yuanrenxue' + window.page)
    // btoa() 是JavaScript内置函数，用于将字符串转换为Base64编码
    // 这里将'yuanrenxue'和页码拼接后进行Base64编码
    // 例如：当page=1时，'yuanrenxue1'编码后变成'eXVhbnJlbnh1ZTE='
};