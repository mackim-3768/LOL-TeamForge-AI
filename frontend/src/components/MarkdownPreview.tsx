import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Box } from '@mui/material';

interface MarkdownPreviewProps {
  content: string;
}

const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({ content }) => {
  if (!content) return null;

  return (
    <Box
      sx={{
        '& h1': { fontSize: '1.5rem', marginTop: 2, marginBottom: 1 },
        '& h2': { fontSize: '1.25rem', marginTop: 2, marginBottom: 1 },
        '& h3': { fontSize: '1.1rem', marginTop: 2, marginBottom: 1 },
        '& p': { marginBottom: 1.0 },
        '& ul, & ol': { paddingLeft: 3, marginBottom: 1.0 },
        '& code': {
          fontFamily: 'monospace',
          backgroundColor: '#f5f5f5',
          padding: '2px 4px',
          borderRadius: 1,
          fontSize: '0.85rem',
        },
        '& pre code': {
          backgroundColor: 'transparent',
          padding: 0,
        },
        '& pre': {
          backgroundColor: '#f5f5f5',
          padding: 1,
          borderRadius: 1,
          overflowX: 'auto',
        },
        '& blockquote': {
          borderLeft: '4px solid #e0e0e0',
          margin: 0,
          marginBottom: 1.0,
          paddingLeft: 2,
          color: 'text.secondary',
        },
      }}
    >
      <ReactMarkdown>{content}</ReactMarkdown>
    </Box>
  );
};

export default MarkdownPreview;
