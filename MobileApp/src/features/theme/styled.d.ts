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
      space2: string;
      space4: string;
      space8: string;
      space16: string;
      space24: string;
      space48: string;
    };
    borderRadius: string;
  }
}
