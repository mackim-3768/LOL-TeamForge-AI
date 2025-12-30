import { AppBar, Toolbar, Typography, Button, Box, IconButton, Container } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import AnalyticsIcon from '@mui/icons-material/Analytics'; // You might need to make sure this exists or pick another
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import SearchIcon from '@mui/icons-material/Search';

export default function Navbar() {
    const location = useLocation();

    const isActive = (path: string) => location.pathname === path;

    return (
        <AppBar position="sticky" color="transparent" elevation={0} sx={{ backdropFilter: 'blur(12px)', borderBottom: '1px solid rgba(255,255,255,0.05)', background: 'rgba(15, 23, 42, 0.6)' }}>
            <Container maxWidth="xl">
                <Toolbar disableGutters sx={{ height: 72 }}>
                    {/* Logo */}
                    <Box sx={{ display: 'flex', alignItems: 'center', mr: 4, textDecoration: 'none', color: 'inherit' }} component={Link} to="/">
                        <Box sx={{
                            width: 36, height: 36, borderRadius: '8px',
                            background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center', mr: 1.5,
                            boxShadow: '0 0 15px rgba(59, 130, 246, 0.5)'
                        }}>
                            <AnalyticsIcon sx={{ color: 'white', fontSize: 20 }} />
                        </Box>
                        <Typography variant="h6" sx={{ fontWeight: 700, letterSpacing: '-0.02em', bg: 'linear-gradient(to right, #fff, #94a3b8)', backgroundClip: 'text' }}>
                            Flex Analyst
                        </Typography>
                    </Box>

                    {/* Nav Links */}
                    <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, gap: 1 }}>
                        {[
                            { label: 'Home', path: '/' },
                            { label: 'Dashboard', path: '/dashboard/demo' }, // Demo link for now
                            { label: 'Team Builder', path: '/team-builder' },
                        ].map((item) => (
                            <Button
                                key={item.path}
                                component={Link}
                                to={item.path}
                                sx={{
                                    color: isActive(item.path) ? 'primary.main' : 'text.secondary',
                                    fontWeight: isActive(item.path) ? 600 : 500,
                                    '&:hover': {
                                        color: 'text.primary',
                                        background: 'rgba(255,255,255,0.03)'
                                    }
                                }}
                            >
                                {item.label}
                            </Button>
                        ))}
                    </Box>

                    {/* Right Actions */}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <IconButton size="small" sx={{ color: 'text.secondary' }}>
                            <SearchIcon fontSize="small" />
                        </IconButton>
                        <Box sx={{ width: 1, height: 24, bgcolor: 'divider', mx: 1 }} />
                        <Button
                            variant="outlined"
                            size="small"
                            startIcon={<AdminPanelSettingsIcon />}
                            sx={{ borderColor: 'rgba(255,255,255,0.1)', color: 'text.secondary' }}
                        >
                            Admin
                        </Button>
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
}
