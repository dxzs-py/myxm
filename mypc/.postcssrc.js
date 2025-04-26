// https://github.com/michael-ciniawsky/postcss-load-config

module.exports = {
  "plugins": {
    "postcss-import": {},
    "postcss-url": {},
    // 要编辑目标浏览器：使用 package.json 中的 “BrowsersList” 字段
    "autoprefixer": {},
    "tailwindcss": {},  // 导入这个插件
  }
}
