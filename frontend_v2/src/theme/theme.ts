import { createTheme, alpha } from '@mui/material/styles';

const primaryColor = '#3b82f6'; // Blue 500
const secondaryColor = '#d4af37'; // Gold
const bgColor = '#0f172a'; // Slate 900
const surfaceColor = '#1e293b'; // Slate 800

export const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: primaryColor,
            contrastText: '#ffffff',
        },
        secondary: {
            main: secondaryColor,
            contrastText: '#0f172a',
        },
        background: {
            default: bgColor,
            paper: surfaceColor,
        },
        text: {
            primary: '#f8fafc',
            secondary: '#94a3b8',
        },
        success: {
            main: '#10b981',
        },
        error: {
            main: '#ef4444',
        },
        warning: {
            main: '#f59e0b',
        },
        info: {
            main: '#0ea5e9',
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h1: { fontSize: '2.5rem', fontWeight: 700, letterSpacing: '-0.02em' },
        h2: { fontSize: '2rem', fontWeight: 700, letterSpacing: '-0.01em' },
        h3: { fontSize: '1.75rem', fontWeight: 600 },
        h4: { fontSize: '1.5rem', fontWeight: 600 },
        h5: { fontSize: '1.25rem', fontWeight: 600 },
        h6: { fontSize: '1rem', fontWeight: 600 },
        subtitle1: { fontSize: '1rem', fontWeight: 500 },
        subtitle2: { fontSize: '0.875rem', fontWeight: 500, color: '#94a3b8' },
        body1: { fontSize: '1rem', lineHeight: 1.6 },
        body2: { fontSize: '0.875rem', lineHeight: 1.6 },
    },
    shape: {
        borderRadius: 12,
    },
    components: {
        MuiCssBaseline: {
            styleOverrides: {
                body: {
                    scrollbarColor: '#334155 #0f172a',
                    '&::-webkit-scrollbar, & *::-webkit-scrollbar': {
                        width: '8px',
                        height: '8px',
                        backgroundColor: '#0f172a',
                    },
                    '&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb': {
                        borderRadius: 8,
                        backgroundColor: '#334155',
                        minHeight: 24,
                        border: '2px solid #0f172a',
                    },
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: 'none',
                    fontWeight: 600,
                    borderRadius: '8px',
                    padding: '8px 16px',
                },
                containedPrimary: {
                    background: `linear-gradient(135deg, ${primaryColor} 0%, #2563eb 100%)`,
                    boxShadow: `0 4px 12px ${alpha(primaryColor, 0.4)}`,
                    '&:hover': {
                        boxShadow: `0 6px 16px ${alpha(primaryColor, 0.6)}`,
                    },
                },
            },
        },
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundImage: 'none',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                },
                elevation1: {
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    borderRadius: 16,
                    background: `linear-gradient(145deg, ${surfaceColor} 0%, ${alpha('#0f172a', 0.9)} 100%)`,
                    backdropFilter: 'blur(10px)',
                },
            },
        },
        MuiChip: {
            styleOverrides: {
                root: {
                    fontWeight: 500,
                },
            },
        },
    },
});
