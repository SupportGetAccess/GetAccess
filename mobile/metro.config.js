const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

config.resolver.sourceExts.push('svg');

// Mock Node.js built-in modules not available in React Native
config.resolver.extraNodeModules = {
  ...config.resolver.extraNodeModules,
  fs: require.resolve('./assets/fs.js'),
};

module.exports = config;
