const webpack = require('webpack');

module.exports = {
    webpack: {
        configure: {
            resolve: {
                fallback: {
                    "assert": require.resolve("assert/"),
                    "util": require.resolve("util/"),
                    "crypto": require.resolve("crypto-browserify"),
                    "stream": require.resolve("stream-browserify"),
                    "url": require.resolve("url/"),
                    "buffer": require.resolve("buffer/"),
                    "path": require.resolve("path-browserify"),
                    "querystring": require.resolve("querystring-es3"),
                    "http": require.resolve("stream-http"),
                    "https": require.resolve("https-browserify"),
                    "zlib": require.resolve("browserify-zlib"),
                    "fs": false,
                    "net": false,
                    "tls": false,
                    "vm": require.resolve("vm-browserify"),
                }
            }
        },
        plugins: [
            new webpack.ProvidePlugin({
                process: 'process/browser',
                Buffer: ['buffer', 'Buffer'],
            }),
        ]
    }
};
