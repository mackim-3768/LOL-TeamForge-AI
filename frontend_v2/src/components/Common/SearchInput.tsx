import { Paper, InputBase, IconButton, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface SearchInputProps {
    initialValue?: string;
    onSearch?: (value: string) => void;
    placeholder?: string;
}

export default function SearchInput({ initialValue = '', onSearch, placeholder = "Enter Summoner Name..." }: SearchInputProps) {
    const [value, setValue] = useState(initialValue);
    const navigate = useNavigate();

    const handleSearch = () => {
        if (!value.trim()) return;
        if (onSearch) {
            onSearch(value);
        } else {
            navigate(`/dashboard/${encodeURIComponent(value.trim())}`);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') handleSearch();
    };

    return (
        <Paper
            elevation={0}
            sx={{
                p: '2px 4px',
                display: 'flex',
                alignItems: 'center',
                width: '100%',
                maxWidth: 600,
                borderRadius: '16px',
                border: '1px solid rgba(255,255,255,0.1)',
                background: 'rgba(30, 41, 59, 0.6)',
                backdropFilter: 'blur(10px)',
                transition: 'all 0.2s ease-in-out',
                '&:hover, &:focus-within': {
                    border: '1px solid rgba(59, 130, 246, 0.5)',
                    boxShadow: '0 0 20px rgba(59, 130, 246, 0.2)',
                    background: 'rgba(30, 41, 59, 0.8)',
                    transform: 'scale(1.01)',
                },
            }}
        >
            <Box sx={{ p: 2, color: 'text.secondary', display: 'flex' }}>
                <SearchIcon />
            </Box>
            <InputBase
                sx={{ ml: 1, flex: 1, fontSize: '1.1rem' }}
                placeholder={placeholder}
                inputProps={{ 'aria-label': 'search summoner' }}
                value={value}
                onChange={(e) => setValue(e.target.value)}
                onKeyDown={handleKeyDown}
                autoFocus
            />
            <IconButton
                color="primary"
                sx={{ p: '10px', m: 0.5, backgroundColor: 'rgba(59, 130, 246, 0.1)', '&:hover': { backgroundColor: 'primary.main', color: 'white' } }}
                aria-label="search"
                onClick={handleSearch}
            >
                <ArrowForwardIcon />
            </IconButton>
        </Paper>
    );
}
