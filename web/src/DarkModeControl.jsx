import React from "react";
import useDarkMode from "use-dark-mode";

export default () => {
  const darkMode = useDarkMode(false)
  return (
    <div className="switch">
      <label className="grey-text text-lighten-5">
        Darkmode
        <input checked={darkMode.value} onChange={darkMode.toggle} type="checkbox" />
        <span className="lever"></span>
      </label>
    </div>
  );
};
