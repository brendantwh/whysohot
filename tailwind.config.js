module.exports = {
  purge: {
    enabled: true,
    content: [
      './templates/*.html',
      './static/*.js',
    ],
  },
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        scheme: {
          100: '#A3BCB9',
          200: '#39603D',
          300: '#555c57',
          350: '#434a45',
          400: '#3C403D',
          450: '#292e2a',
          500: '#fdfffa',
          525: '#f6f7f2',
          550: '#eff2e9',
          600: '#e8eddf',
          700: '#DADED4',
          800: '#bbc2b0',
        },
        uvi: {
          l: {
            100: '#d6dbb8',
            200: '#dbdbb8',
            300: '#dbceb8',
            400: '#dbc0b8',
            500: '#c2b8db',
          },
          d: {
            100: '#667350',
            200: '#7a7a4e',
            300: '#96804e',
            400: '#8c6053',
            500: '#59506e',
          }
        },
        dark: {
          100: '#13171e',
          150: '#1e1f29',
          175: '#26253A',
          200: '#2A2D41',
          205: '#C0B5DE',
          210: '#FAF7EC',
          225: '#4C6274',
          250: '#634B50',
          275: '#36434D',
          300: '#47464e',
          400: '#A0AEB6',
          500: '#f88090',
          525: '#f89aa6',
          575: '#b28784',
          600: '#DBB9B3',
          700: '#DEB2AD',
        },
        pin: {
          100: '#79b522',
          200: '#5f5b87',
        }
      },
      fontFamily: {
        body: ['Inter'],
        title: ['Mali'],
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
