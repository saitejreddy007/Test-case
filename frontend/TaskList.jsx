import React, { useState } from 'react';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [taskInput, setTaskInput] = useState('');

  const addTask = () => {
    if (taskInput) {
      setTasks([...tasks, taskInput]);
      setTaskInput('');
    }
  };

  return (
    <div>
      <h1>Task List</h1>
      <input
        type='text'
        value={taskInput}
        onChange={(e) => setTaskInput(e.target.value)}
        placeholder='Add a new task'
      />
      <button onClick={addTask}>Add Task</button>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>{task}</li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;