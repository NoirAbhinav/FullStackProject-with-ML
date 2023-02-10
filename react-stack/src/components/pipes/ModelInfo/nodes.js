import ReactFlow, { Controls, Background, MarkerType } from "reactflow";
import React from "react";
import ApiOnClick from "../apiCalls";
import { FingerPrintContext } from "../fingerContext";
import "reactflow/dist/style.css";
import { Box, CircularProgress, Modal, Typography } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
const proOptions = { hideAttribution: true };
const style_box = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  height: 180,
  width: 250,
  margin: 1,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
  opacity: 4,
  textAlign: "center",
};

export default function Flow() {
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
  let data_ref = [];
  let edge_ref = [];
  let color_dict = {
    Conv2D: "#fdd267",
    BatchNormalization: "#dc325c",
    MaxPooling2D: "#00c48d",
    Dropout: "#0b8cac",
    Flatten: "#063b4b",
    Dense: "#fdd267",
  };
  let font_dict = {
    Conv2D: "#000000",
    BatchNormalization: "#000000",
    MaxPooling2D: "#000000",
    Dropout: "#000000",
    Flatten: "#FFFFFF",
    Dense: "#000000",
  };
  const [clck, setClck] = React.useState(null);
  const clickhandler = (event, node) => {
    setClck(node.id);
  };
  let xmul = 0;
  let ymul = 0;

  return (
    <>
      {!data && (
        <CircularProgress color="secondary" sx={{ position: "unset" }} />
      )}
      {data && (
        <div>
          <img
            width="1600"
            height="200"
            src={`data:image/jpg;base64,${data[0]}`}
            style={{ display: "flex" }}
          />
        </div>
      )}

      {data && (
        <div
          style={{
            width: 1600,
            height: 200,
            display: "flex",
            position: "fixed",
            top: "30rem",
          }}
        >
          {Object.values(data[1]).map((row, index) => {
            if (index % 2 == 0) {
              xmul = 100 * index;
              ymul = 0;
            } else {
              xmul = 100 * (index - 1);
              ymul = 100;
            }
            data_ref.push({
              id: `${index}`,
              data: { label: row.Type },
              position: { x: xmul, y: ymul },
              style: {
                color: `${font_dict[row.Type]}`,
                backgroundColor: `${color_dict[row.Type]}`,
              },
            });
            edge_ref.push({
              id: `${index}->${index + 1}`,
              source: `${index}`,
              target: `${index + 1}`,
              type: "step",
              markerEnd: {
                type: MarkerType.Arrow,
                width: 20,
                height: 20,
                color: "#FF0072",
              },
              style: {
                strokeWidth: 2,
                stroke: "#FF0072",
              },
            });
            // setNodedt((oldNodedt) => [
            //   ...oldNodedt,
            //   {
            //     id: `${index}`,
            //     data: `{label:${row.Type}}`,
            //     position: `{ x: ${50 * index}, y: ${50 * index} },`,
            //   },
            // ]);
          })}
          {console.log(data_ref)}
          {data_ref && (
            <p style={{ flex: "auto" }}>
              <Typography>Click on the nodes to get more info:</Typography>
              <br />
              <ReactFlow
                nodes={data_ref}
                edges={edge_ref}
                onNodeClick={clickhandler}
                proOptions={proOptions}
                fitView={true}
                style={{
                  position: "relative",
                  border: "2px solid #000",
                }}
              >
                <Background />
              </ReactFlow>
            </p>
          )}
          {clck && (
            <Modal
              open={clck + 1}
              onClose={() => {
                setClck(false);
              }}
            >
              <Box sx={style_box}>
                <CloseIcon
                  onClick={() => {
                    setClck(false);
                  }}
                  sx={{
                    display: "flex",
                    position: "relative",
                    left: "255px",
                    top: "-30px",
                    color: "white",
                    backgroundColor: "black",
                    borderRadius: "16px",
                  }}
                />
                <>
                  <Typography>Layer Type:{data[1][clck].Type}</Typography>
                  <Typography>
                    Layer Shape:{JSON.stringify(data[1][clck].Shape, null, 2)}
                  </Typography>
                  <Typography>
                    Layer Trainable Params:{data[1][clck].Param}
                  </Typography>
                </>
              </Box>
            </Modal>
            // <div style={{ display: "flex", position: "fixed", top: "50rem" }}>
            //   {console.log(clck)}
            //
            // </div>
          )}
        </div>
      )}
    </>
  );
}
