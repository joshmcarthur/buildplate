import React from "react";
import DarkModeControl from "./DarkModeControl";

export default () => (
  <nav className="nav-extended">
    <div className="nav-wrapper row">
      <div className="col s12">
        <a href="/" className="brand-logo">Buildplate</a>
        <div className="right">
          <DarkModeControl />
        </div>
      </div>
    </div>
  </nav>
);
