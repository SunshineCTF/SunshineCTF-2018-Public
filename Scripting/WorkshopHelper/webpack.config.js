const HTMLWebpackPlugin = require('html-webpack-plugin');
const HTMLWebpackPluginConfig = new HTMLWebpackPlugin({
  template: __dirname + '/www/index.html',
  filename: 'index.html',
  // inject: 'body',
});

module.exports = {
  entry: __dirname + '/app/App.js',
  module: {
    rules: [
      {
        test: /\.js$/,
        include: /app/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        include: /app/,
        use: ['style-loader', 'css-loader']
        /*{
          loader: 'url-loader',
          options: {
            limit: 8000,
            name: 'images/[hash]-[name].ext'
          }
        }
        ] // */
      },
      {
        test: /\.(png|jp(e*)g|svg)$/,  
        include: /app/,
        // use: 'url-loader'
        use: [{
            loader: 'file-loader',
            // options: { 
            //     limit: 8000, // Convert images < 8kb to base64 strings
            //     name: 'images/[hash]-[name].[ext]'
            // } 
        }]
      }
    ]
  },
  output: {
    filename: 'bundle.js',
    path: __dirname + '/www/'
  },
  plugins: [HTMLWebpackPluginConfig],
  mode: 'production'
}