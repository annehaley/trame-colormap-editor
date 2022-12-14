const { defineConfig } = require("@vue/cli-service");

const path = require("path");
const DST_PATH = "../trame_app/module/serve";

module.exports = defineConfig({
  transpileDependencies: ["vuetify"],
  outputDir: path.resolve(__dirname, DST_PATH),
});
