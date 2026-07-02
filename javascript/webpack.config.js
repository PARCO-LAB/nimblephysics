const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

const sharedRules = [
  {
    test: /\.(js|ts)$/,
    exclude: /node_modules/,
    use: ["babel-loader"],
  },
  {
    test: /\.s[ac]ss$/i,
    use: ["style-loader", "css-loader", "sass-loader"],
  },
  { test: /\.svg$/i, type: "asset/source" },
  { test: /\.(bin|gz)$/i, type: "asset/resource" },
  { test: /\.txt$/i, type: "asset/source" },
];

const entriesByTarget = {
  package: {
    NimbleStandaloneReact: "./src/NimbleStandaloneReact.ts",
    NimbleStandalone: "./src/NimbleStandalone.ts",
    NimbleRemote: "./src/NimbleRemote.ts",
  },
  python: {
    live: "./src/live.ts",
    embeddable: "./src/embedded.ts",
  },
  dev: {
    embedded_dev: "./src/embedded_dev.ts",
    NimbleStandaloneReact: "./src/NimbleStandaloneReact.ts",
    NimbleStandalone: "./src/NimbleStandalone.ts",
    NimbleRemote: "./src/NimbleRemote.ts",
  },
  "dev-python": {
    live: "./src/live.ts",
    NimbleStandaloneReact: "./src/NimbleStandaloneReact.ts",
    NimbleStandalone: "./src/NimbleStandalone.ts",
    NimbleRemote: "./src/NimbleRemote.ts",
  },
  "dev-screenshot": {
    screenshot: "./src/NimbleScreenshot.ts",
    NimbleStandaloneReact: "./src/NimbleStandaloneReact.ts",
    NimbleStandalone: "./src/NimbleStandalone.ts",
    NimbleRemote: "./src/NimbleRemote.ts",
  },
};

const configByTarget = {
  package: { mode: "production" },
  python: { mode: "production" },
  dev: { mode: "development", devServer: true },
  "dev-python": { mode: "development", devServer: true },
  "dev-screenshot": { mode: "development", devServer: true },
};

module.exports = (_env = {}) => {
  const target = _env.target || "package";
  const config = configByTarget[target] || configByTarget.package;
  const entries = entriesByTarget[target] || entriesByTarget.package;

  const htmlPluginOptions = {
    template: path.join(__dirname, "src", "index.html"),
  };
  if (target === "package") {
    htmlPluginOptions.excludeChunks = ["embedded", "live"];
  }
  if (target === "dev-python") {
    htmlPluginOptions.excludeChunks = ["embedded", "live"];
  }
  if (target === "dev-screenshot") {
    htmlPluginOptions.excludeChunks = ["embedded", "live"];
  }

  const result = {
    entry: entries,
    module: { rules: sharedRules },
    resolve: { extensions: ["*", ".ts", ".js"] },
    output: {
      path: path.join(__dirname, "dist"),
      publicPath: "/",
      filename: "[name].js",
      library: "[name]",
      libraryTarget: "umd",
    },
    externals: target === "package" || target === "python" ? { react: "commonjs2 react" } : undefined,
    plugins: [new HtmlWebpackPlugin(htmlPluginOptions)],
    mode: config.mode,
  };

  if (config.devServer) {
    result.devServer = {
      static: path.join(__dirname, "dist"),
      client: { overlay: { warnings: false, errors: true } },
      port: 9000,
    };
  }

  return result;
};
