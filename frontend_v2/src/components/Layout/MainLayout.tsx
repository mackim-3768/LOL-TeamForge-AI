import { Box } from '@mui/material';
import Navbar from './Navbar';
import type { ReactNode } from 'react';

interface MainLayoutProps {
    children: ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
    return (
        <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            <Navbar />
            <Box component="main" sx={{ flexGrow: 1, position: 'relative' }}>
                {/* Background Mesh/Glow Effects */}
                <Box
                    sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        height: '600px',
                        background: 'radial-gradient(circle at 50% 0%, rgba(59, 130, 246, 0.15) 0%, transparent 70%)',
                        pointerEvents: 'none',
                        zIndex: -1,
                    }}
                />
                {children}
            </Box>
            <Box sx={{ py: 4, textAlign: 'center', color: 'text.secondary', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                <Box sx={{ fontSize: '0.875rem' }}>
                    LoL Flex Rank Analyst © {new Date().getFullYear()}
                </Box>
            </Box>
        </Box>
    );
}
