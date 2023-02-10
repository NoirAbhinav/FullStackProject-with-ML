import React, { Children, createContext } from "react";

export const FingerPrintContext = createContext({
  fingerPrint: "",
  setFingerprint: () => {},
  getFingerprint: () => {},
});

const FingerprintProvider = ({ children }) => {
  const [fingerPrint, setFingerprint] = React.useState(null);
  const getFingerprint = () => {
    return fingerPrint;
  };

  const value = {
    fingerPrint: fingerPrint,
    setFingerprint: setFingerprint,
    getFingerprint: getFingerprint,
  };

  return (
    <FingerPrintContext.Provider value={value}>
      {children}
    </FingerPrintContext.Provider>
  );
};

export default FingerprintProvider;
