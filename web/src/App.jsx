import React, { useState, useEffect } from "react";
import "./App.scss";
import Navbar from "./Navbar";
import ProjectCard from "./ProjectCard";
import "materialize-css";

function App() {
  const [projects, setProjects] = useState([]);
  useEffect(
    () =>
      fetch("/api/projects")
        .then((r) => r.json())
        .then(setProjects) && undefined,
    []
  );

  return (
    <div className="App">
      <Navbar />
      <div className="row">
        {projects.map((project) => (
          <div key={project.name} className="col s12 m6 l3">
            <ProjectCard project={project} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
