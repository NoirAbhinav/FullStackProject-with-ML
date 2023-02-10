import ApiOnClick from "../apiCalls";
import React from "react";
import CloseIcon from "@mui/icons-material/Close";
import {
  Box,
  Button,
  Card,
  CardContent,
  CardMedia,
  CircularProgress,
  Grid,
  Modal,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { FingerPrintContext } from "../fingerContext";
import "./edaPipes.css";
const style_box = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  height: 180,
  width: 200,
  margin: 1,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
  opacity: 4,
  textAlign: "center",
};

export default function TransformData() {
  const fingerContext = React.useContext(FingerPrintContext);
  const [data, setData] = React.useState("");
  const [show, setShow] = React.useState(false);
  React.useEffect(() => {
    async function getData() {
      const data = await ApiOnClick(
        "model/EDA",
        fingerContext.getFingerprint()
      );
      setData(data);
      setShow(true);
    }
    getData();
  }, []);
  {
    console.log(data);
  }
  return <FetchData data={data} show={show} />;
}

function FetchData({ data, show }) {
  let colors = ["red", "purple", "orange", "green", "blue", "yellow", "grey"];
  const [hvr, setHvr] = React.useState(false);
  const style1 = {
    display: "block",
    whiteSpace: "nowrap",
    width: "600px",
    overflowX: "auto",
  };
  return (
    <>
      {!data && (
        <CircularProgress color="secondary" sx={{ position: "unset" }} />
      )}
      {data && (
        <div
          className={`cont ${show ? "showData" : ""}`}
          style={{
            justifySelf: "center",
          }}
        >
          {/* <Typography
            sx={{
              display: "flex",
              position: "absolute",
              top: "-20px",
              transitionDelay: "500ms",
            }}
          >
            Time Taken for Task Completion:{data[1]}(s)
          </Typography> */}
          <Typography
            variant="h4"
            style={{
              position: "relative",
              marginBottom: "10px",
              textAlign: "center",
            }}
          >
            Dataset Overview:
          </Typography>
          <TableContainer
            sx={{
              boxShadow: "10px",
              display: "flex",
              position: "relative",
              left: "8rem",
              width: "810px",
            }}
          >
            <Table sx={{ minWidth: 450 }} aria-label="customized table">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ backgroundColor: "black", color: "white" }}>
                    Emotions
                  </TableCell>
                  <TableCell
                    align="center"
                    sx={{ backgroundColor: "black", color: "white" }}
                  >
                    Pixels
                  </TableCell>
                  <TableCell
                    align="center"
                    sx={{ backgroundColor: "black", color: "white" }}
                  >
                    Usage
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {Object.values(data[0]).map((row, index) => (
                  <>
                    <TableRow className="rowData">
                      <TableCell align="center" scope="row">
                        {row.emotions}
                      </TableCell>
                      <TableCell
                        align="right"
                        onClick={() => {
                          setHvr(index);
                        }}
                        sx={style1}
                      >
                        {JSON.stringify(row.pixels, null, 2)}
                      </TableCell>
                      <TableCell align="center" sx={{ border: "10" }}>
                        {row.Usage}
                      </TableCell>
                    </TableRow>
                  </>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <div className="ddescript">
            <Typography variant="h5" fontFamily="sans-serif">
              Train Test Split:
            </Typography>
            <ul>
              {Object.keys(data[2]).map((n) => (
                <li>
                  <Typography variant="h6">
                    {n}:{data[2][n]}
                  </Typography>
                </li>
              ))}
            </ul>
          </div>
          {console.log(hvr)}
          {hvr !== false && (
            <div className="pixelPrev">
              <Modal
                open={hvr + 1}
                onClose={() => {
                  setHvr(false);
                }}
              >
                <Box sx={style_box}>
                  <CloseIcon
                    onClick={() => {
                      setHvr(false);
                    }}
                    sx={{
                      display: "flex",
                      position: "relative",
                      left: "205px",
                      top: "-30px",
                      color: "white",
                      backgroundColor: "black",
                      borderRadius: "16px",
                    }}
                  />
                  <img
                    width="200"
                    height="200"
                    src={`data:image/jpg;base64,${data[1][hvr]}`}
                    style={{ position: "relative", top: "-30px " }}
                  />
                </Box>
              </Modal>
            </div>
          )}
          <Grid
            container
            direction="row"
            sx={{
              display: "flex",
              position: "relative",
              top: "-6rem",
              gap: "10px",
            }}
          >
            {data[3].map((n, index) => (
              <div className="Container ">
                <div className="dataImg">
                  <Card
                    elevation={0}
                    sx={{
                      "&:hover": {
                        boxShadow: "5px 5px " + colors[index],
                      },
                    }}
                  >
                    <CardMedia>
                      <img
                        width="150"
                        height="150"
                        src={`data:image/jpg;base64,${n}`}
                      />
                    </CardMedia>
                    <CardContent
                      sx={{ display: "flex", justifyContent: "center" }}
                    >
                      <Typography variant="button" fontFamily={"Roboto"}>
                        {Object.keys(data[4])[index]}
                      </Typography>
                    </CardContent>
                  </Card>
                </div>
                <Box boxShadow={5} className="info">
                  <Typography variant="button" fontFamily={"Roboto"}>
                    Category:{Object.keys(data[4])[index]}
                    <br />
                    Count:{Object.values(data[4])[index]}
                    <br />
                    Dimensions:48*48
                  </Typography>
                </Box>
              </div>
            ))}
          </Grid>
        </div>
      )}
    </>
  );
}
