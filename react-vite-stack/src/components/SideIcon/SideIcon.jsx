import * as React from "react";
import Stack from "@mui/material/Stack";
import { IconButton, Typography } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import Box from "@material-ui/core/Box";
import KaggleIcon from "../../logos/kaggle-logo.png";
import "./SideIcon.css";

export default function ResponsiveSideBar() {
  return (
    <div className="container">
      <Box
        display="flex"
        justifyContent="left"
        alignItems="center"
        shadows="10"
        sx={{
          width: 50,
          height: 200,
          backgroundColor: "#000",
          borderRadius: "16px",
        }}
      >
        <Stack spacing={0}>
          <IconButton aria-label="primary" size="large">
            <a
              href="https://github.com/NoirAbhinav"
              target="_blank"
              rel="noopener noreferrer"
            >
              <GitHubIcon style={{ fontSize: 30, color: "white" }} />
            </a>
          </IconButton>
          <IconButton aria-label="primary" size="large">
            <a
              href="https://in.linkedin.com/in/abhinav-nair-n3747"
              target="_blank"
              rel="noopener noreferrer"
            >
              <LinkedInIcon style={{ fontSize: 30 }} color="primary" />
            </a>
          </IconButton>
          <IconButton aria-label="primary" size="large">
            <a
              href="https://www.kaggle.com/noir3747"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img src={KaggleIcon} width="30" height="30" alt=""></img>
            </a>
          </IconButton>
        </Stack>
      </Box>
    </div>
  );
}
