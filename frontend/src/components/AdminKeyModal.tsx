import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Typography } from '@mui/material';
import { api } from '../api';

interface AdminKeyModalProps {
  open: boolean;
  onClose: () => void;
}

const AdminKeyModal: React.FC<AdminKeyModalProps> = ({ open, onClose }) => {
  const [apiKey, setApiKey] = useState('');
  const [openaiKey, setOpenaiKey] = useState('');
  const [loadingRiot, setLoadingRiot] = useState(false);
  const [loadingOpenAI, setLoadingOpenAI] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const handleSaveRiot = async () => {
    if (!apiKey) return;
    setLoadingRiot(true);
    setMessage(null);
    try {
      await api.updateRiotKey(apiKey);
      setMessage({ text: 'Riot API Key updated successfully!', type: 'success' });
      setTimeout(() => {
          onClose();
          setMessage(null);
          setApiKey('');
          setOpenaiKey('');
      }, 1500);
    } catch (err) {
      console.error(err);
      setMessage({ text: 'Failed to update Riot API Key.', type: 'error' });
    } finally {
      setLoadingRiot(false);
    }
  };

  const handleSaveOpenAI = async () => {
    if (!openaiKey) return;
    setLoadingOpenAI(true);
    setMessage(null);
    try {
      await api.updateOpenAIKey(openaiKey);
      setMessage({ text: 'OpenAI API Key updated successfully!', type: 'success' });
      setTimeout(() => {
          onClose();
          setMessage(null);
          setApiKey('');
          setOpenaiKey('');
      }, 1500);
    } catch (err) {
      console.error(err);
      setMessage({ text: 'Failed to update OpenAI API Key.', type: 'error' });
    } finally {
      setLoadingOpenAI(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Admin Configuration</DialogTitle>
      <DialogContent>
        <Typography variant="body2" gutterBottom>
            Enter a valid Riot API Key to enable summoner registration and data collection.
        </Typography>
        <TextField
          autoFocus
          margin="dense"
          id="api-key"
          label="Riot API Key"
          type="password"
          fullWidth
          variant="outlined"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
        <Button onClick={handleSaveRiot} variant="contained" color="primary" disabled={loadingRiot} sx={{ mt: 2 }}>
          {loadingRiot ? 'Saving...' : 'Save Riot API Key'}
        </Button>

        <Typography variant="body2" gutterBottom style={{ marginTop: '24px' }}>
            Enter your OpenAI API Key to enable AI-based analysis and recommendations.
        </Typography>
        <TextField
          margin="dense"
          id="openai-api-key"
          label="OpenAI API Key"
          type="password"
          fullWidth
          variant="outlined"
          value={openaiKey}
          onChange={(e) => setOpenaiKey(e.target.value)}
        />
        <Button onClick={handleSaveOpenAI} variant="contained" color="primary" disabled={loadingOpenAI} sx={{ mt: 2 }}>
          {loadingOpenAI ? 'Saving...' : 'Save OpenAI API Key'}
        </Button>
        {message && (
          <Typography color={message.type} style={{ marginTop: '10px' }}>
            {message.text}
          </Typography>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="inherit">Cancel</Button>
      </DialogActions>
    </Dialog>
  );
};

export default AdminKeyModal;
