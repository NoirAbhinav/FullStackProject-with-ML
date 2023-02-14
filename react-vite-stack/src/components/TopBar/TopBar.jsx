import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import "./TopBar.css";
import EmotionDetect from "../EmotionPipelines/Pipes";
import Demo from "../Demo/demo";

const buttonStyles = { color: "white", "&:hover": { color: "red" } };
export default function ResponsiveTopBar() {
  const [demo, setDemo] = React.useState(false);
  return (
    <>
      <div className="topbar">
        <AppBar
          position="static"
          sx={{ alignSelf: "center" }}
          color="transparent"
          elevation="0px"
        >
          <Box
            sx={{
              flexGrow: 1,
              alignSelf: "center",
              borderRadius: "0 0 16px 16px",
            }}
            boxShadow={3}
            color="transparent"
          >
            <Toolbar
              sx={{
                backgroundColor: "black",
                justifyContent: "center",
                borderRadius: "inherit",
              }}
              sizeHeight="10px"
              elevation={10}
            >
              {/* <IconButton sx={buttonStyles}>
              <Typography variant="h6" component="div">
                About Me
              </Typography>
            </IconButton>
            <IconButton sx={buttonStyles}>
              <Typography variant="h6" component="div">
                Projects
              </Typography>
            </IconButton>
            <IconButton sx={buttonStyles}>
              <Typography variant="h6" component="div">
                Skillset
              </Typography>
            </IconButton> */}
              <IconButton sx={buttonStyles} onClick={() => setDemo(!demo)}>
                <Typography variant="h6" component="div">
                  Live Demo
                </Typography>
              </IconButton>
            </Toolbar>
          </Box>
        </AppBar>
      </div>
      <div>{demo && <Demo />}</div>
    </>
  );
}
