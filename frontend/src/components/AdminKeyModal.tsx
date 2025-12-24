import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Typography } from '@mui/material';
import { api } from '../api';

interface AdminKeyModalProps {
  open: boolean;
  onClose: () => void;
}

const AdminKeyModal: React.FC<AdminKeyModalProps> = ({ open, onClose }) => {
  const [apiKey, setApiKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const handleSave = async () => {
    if (!apiKey) return;
    setLoading(true);
    setMessage(null);
    try {
      await api.updateRiotKey(apiKey);
      setMessage({ text: 'API Key updated successfully!', type: 'success' });
      setTimeout(() => {
          onClose();
          setMessage(null);
          setApiKey('');
      }, 1500);
    } catch (err) {
      console.error(err);
      setMessage({ text: 'Failed to update API Key.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Update Riot API Key</DialogTitle>
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
        {message && (
          <Typography color={message.type} style={{ marginTop: '10px' }}>
            {message.text}
          </Typography>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="inherit">Cancel</Button>
        <Button onClick={handleSave} variant="contained" color="primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AdminKeyModal;
