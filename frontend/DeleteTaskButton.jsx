import React from 'react';

const TaskItem = ({ task, onDelete }) => {
  return (
    <div>
      <span>{task.name}</span>
      <button onClick={() => onDelete(task.id)}>Delete</button>
    </div>
  );
};

const TaskList = ({ tasks, setTasks }) => {
  const handleDelete = (id) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  return (
    <div>
      {tasks.map(task => (
        <TaskItem key={task.id} task={task} onDelete={handleDelete} />
      ))}
    </div>
  );
};

export default TaskList;