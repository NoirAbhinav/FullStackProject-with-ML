import * as React from 'react';
import Stack from '@mui/material/Stack';
import { IconButton } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import Box from "@material-ui/core/Box";
import KaggleIcon from './logos/kaggle-logo.png'
export default function ResponsiveAppBar() {
  return (    
        <Box
            display="flex"
            justifyContent="left"
            alignItems="center"
            minHeight="100vh"
        >
      <Stack
        spacing={0}
      >
     <IconButton aria-label="primary" sx = {{width:'10px'}} size = "large">
        <GitHubIcon/>
      </IconButton>
      <IconButton aria-label="primary" sx = {{width:'10px'}}>
        <LinkedInIcon/>
      </IconButton>
      <IconButton aria-label="primary" sx = {{width:'10px'}}>
        <img src = {KaggleIcon} width="25" height="25"></img>
      </IconButton>
    </Stack>
    </Box>
  );
}