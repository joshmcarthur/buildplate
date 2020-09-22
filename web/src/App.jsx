import React, { useState, useEffect } from "react";
import "./App.scss";
import Navbar from "./Navbar";
import ProjectCard from "./ProjectCard";
import ProjectCreate from "./ProjectCreate";
import "materialize-css";

function App() {
  const [projects, setProjects] = useState([]);
  const fetchProjects = () =>
    fetch("/api/projects")
      .then((r) => r.json())
      .then(setProjects);

  useEffect(() => fetchProjects() && undefined, []);

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

      <ProjectCreate onCreate={fetchProjects} />
    </div>
  );
}

export default App;
