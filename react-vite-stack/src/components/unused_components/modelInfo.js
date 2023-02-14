import React from "react";
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
import ApiOnClick from "../apiCalls";
export default function ModelInfo() {
  const fingerContext = React.useContext(FingerPrintContext);
  const [data, setData] = React.useState("");
  const [show, setShow] = React.useState(false);
  React.useEffect(() => {
    async function getData() {
      const data = await ApiOnClick(
        "model/modelInfo",
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
  console.log(data);
  let color_dict = {
    Conv2D: "#fdd267",
    BatchNormalization: "#dc325c",
    MaxPooling2D: "#00c48d",
    Dropout: "#00c48d",
    Flatten: "#00c48d",
    Dense: "#fdd267",
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
          <Typography
            variant="h4"
            style={{
              position: "relative",
              marginBottom: "10px",
              textAlign: "center",
            }}
          >
            Model Overview:
          </Typography>
          <TableContainer
            sx={{
              boxShadow: "10px",
              display: "flex",
              position: "relative",
              left: "23rem",
              width: "810px",
            }}
          >
            <Table sx={{ minWidth: 450 }} aria-label="customized table">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ backgroundColor: "black", color: "white" }}>
                    Param
                  </TableCell>
                  <TableCell
                    align="center"
                    sx={{ backgroundColor: "black", color: "white" }}
                  >
                    Shape
                  </TableCell>
                  <TableCell
                    align="center"
                    sx={{ backgroundColor: "black", color: "white" }}
                  >
                    Type
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {Object.values(data[1]).map((row) => (
                  <>
                    <TableRow
                      className="rowData"
                      sx={{ backgroundColor: `${color_dict[row.Type]}` }}
                    >
                      <TableCell align="center" scope="row">
                        {row.Param}
                      </TableCell>
                      <TableCell align="center">{row.Shape}</TableCell>
                      <TableCell align="center" sx={{ border: "10" }}>
                        {row.Type}
                      </TableCell>
                    </TableRow>
                  </>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      )}
    </>
  );
}
