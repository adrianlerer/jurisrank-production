import typescript from 'rollup-plugin-typescript2';

export default [
  // CommonJS build
  {
    input: 'src/index.ts',
    output: {
      file: 'dist/index.js',
      format: 'cjs',
      sourcemap: true,
      exports: 'named'
    },
    plugins: [
      typescript({
        typescript: require('typescript'),
        tsconfig: 'tsconfig.json',
        tsconfigOverride: {
          compilerOptions: {
            module: 'CommonJS',
            declaration: true,
            declarationDir: 'dist'
          }
        }
      })
    ],
    external: ['axios']
  },
  // ES Module build
  {
    input: 'src/index.ts',
    output: {
      file: 'dist/index.esm.js',
      format: 'es',
      sourcemap: true
    },
    plugins: [
      typescript({
        typescript: require('typescript'),
        tsconfig: 'tsconfig.json',
        tsconfigOverride: {
          compilerOptions: {
            module: 'ESNext',
            declaration: false
          }
        }
      })
    ],
    external: ['axios']
  }
];