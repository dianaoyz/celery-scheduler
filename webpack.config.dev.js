const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const dotenv = require('dotenv').config({path: 'config/docker/development/.env'});

// call dotenv and it will return an Object with a parsed key 
const env = dotenv.parsed;

// reduce it to a nice object, the same as before
const envKeys = Object.keys(env).reduce((prev, next) => {
prev[`process.env.${next}`] = JSON.stringify(env[next]);
return prev;
}, {});

console.log(process.env.RACES_SERVICE_URL);

const config = {
    entry:  __dirname + '/static/js/index.jsx',
    output: {
        path: __dirname + '/static/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: [".js", ".jsx", ".css"]
    },
    module: {
        rules: [
            {
                test: /\.jsx?/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            {
                test: /\.css$/,
                use: ['style-loader', MiniCssExtractPlugin.loader, 'css-loader']
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: 'file-loader'
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            path: __dirname + '/static/dist',
            filename: 'styles.css',
        }),
        new webpack.DefinePlugin(envKeys)
    ]
};

module.exports = config;
