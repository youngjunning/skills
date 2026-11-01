export const qingshanTheme = {
  light: {
    background: '#F4F6F1',
    surface: '#FBFCFA',
    surfaceMuted: '#E8EEEA',
    text: '#183B40',
    textSecondary: '#4D676B',
    primary: '#2E948A',
    primaryAction: '#286B66',
    onPrimaryAction: '#FFFFFF',
    primaryContainer: '#DCEFEB',
    success: '#356439',
    warning: '#7A5B1E',
    error: '#8E493E',
    border: '#D4DFDC',
    focus: '#286B66',
  },
  dark: {
    background: '#0F2B36',
    surface: '#183B40',
    surfaceMuted: '#234B50',
    text: '#F2F7F2',
    textSecondary: '#B8CCDB',
    primary: '#85C7BA',
    primaryAction: '#85C7BA',
    onPrimaryAction: '#0F2B36',
    primaryContainer: '#286B66',
    success: '#9BC79E',
    warning: '#E5C47B',
    error: '#E5A394',
    border: '#607D80',
    focus: '#85C7BA',
  },
  spacing: {
    micro: 4,
    small: 8,
    medium: 16,
    large: 24,
    section: 32,
  },
  radius: {
    control: 10,
    surface: 16,
    expressive: 20,
  },
  typography: {
    body: 16,
    bodyLineHeight: 24,
    label: 14,
    title: 24,
    titleLineHeight: 32,
  },
  breakpoints: {
    compactMax: 599,
    mediumMax: 839,
  },
  minimumTarget: {
    ios: 44,
    android: 48,
  },
  state: {
    disabledOpacity: 0.48,
    pressedOpacity: 0.84,
    focusWidth: 2,
    scrimOpacity: 0.36,
  },
  elevation: {
    resting: 0,
    floating: 4,
    modal: 12,
  },
  motion: {
    fast: 140,
    normal: 200,
    narrative: 550,
  },
} as const;

export type QingshanTheme = typeof qingshanTheme;
export type QingshanColorScheme =
  (typeof qingshanTheme)['light' | 'dark'];
