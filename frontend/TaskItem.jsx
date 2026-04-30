const TaskItem = ({ task, onTaskUpdated, onTaskDeleted }) => {
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [isEditing, setIsEditing] = React.useState(false);
  const [editedTitle, setEditedTitle] = React.useState(task.title);

  const handleEdit = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:5000/api/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: editedTitle, completed: task.completed })
      });
      if (!response.ok) throw new Error('Failed to update task');
      const updatedTask = await response.json();
      onTaskUpdated(updatedTask);
      setIsEditing(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:5000/api/tasks/${task.id}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('Failed to delete task');
      onTaskDeleted(task.id);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      backgroundColor: '#FFFFFF',
      borderRadius: '8px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      padding: '16px',
      margin: '16px 0',
      transition: 'all 0.2s ease',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'relative'
    }}>
      {isLoading ? (
        <div style={{
          width: '100%',
          height: '20px',
          backgroundColor: '#E2E8F0',
          borderRadius: '4px',
          animation: 'pulse 1.5s infinite'
        }} />
      ) : (
        <>
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => handleEdit()}
            aria-label={`Mark ${task.title} as completed`}
            style={{ marginRight: '16px' }}
          />
          {isEditing ? (
            <input
              type="text"
              value={editedTitle}
              onChange={(e) => setEditedTitle(e.target.value)}
              style={{
                flex: 1,
                padding: '12px',
                border: '1px solid #E2E8F0',
                borderRadius: '6px',
                marginRight: '16px',
                outline: 'none',
                transition: 'border-color 0.2s ease',
              }}
              onFocus={(e) => e.target.style.borderColor = '#4F46E5'}
              onBlur={(e) => e.target.style.borderColor = '#E2E8F0'}
            />
          ) : (
            <span style={{ fontWeight: '600', color: '#1E293B' }}>{task.title}</span>
          )}
          <div>
            <button
              onClick={() => setIsEditing(!isEditing)}
              aria-label={isEditing ? 'Save changes' : 'Edit task'}
              style={{
                background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                padding: '8px 16px',
                cursor: 'pointer',
                marginRight: '8px',
                transition: 'all 0.2s ease',
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#3B3F9A'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = ''}
            >
              {isEditing ? 'Save' : 'Edit'}
            </button>
            <button
              onClick={handleDelete}
              aria-label='Delete task'
              style={{
                backgroundColor: '#EF4444',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                padding: '8px 16px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#C53030'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = ''}
            >
              Delete
            </button>
          </div>
          {error && <div style={{ color: '#EF4444', marginTop: '8px' }}>{error}</div>}
        </>
      )}
    </div>
  );
};

export default TaskItem;