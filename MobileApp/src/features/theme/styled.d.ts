import 'styled-components/native';

declare module 'styled-components/native' {
  export interface DefaultTheme {
    colors: {
      primary: string;
      secondary: string;
      tertiary: string;
      background: string;
      gray: string;
    };
    fontSizes: {
      small: string;
      medium: string;
      large: string;
      extralarge: string;
    };
    spaces: {
      space4: string;
      space8: string;
      space16: string;
      space48: string;
    };
  }
}
