const TaskList = () => {
  const [tasks, setTasks] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  const fetchTasks = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/tasks');
      if (!response.ok) throw new Error('Failed to fetch tasks');
      const data = await response.json();
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    fetchTasks();
  }, []);

  const handleToggleCompletion = async (taskId) => {
    const updatedTasks = tasks.map(task => 
      task.id === taskId ? { ...task, completed: !task.completed } : task
    );
    setTasks(updatedTasks);
    // Optimistic update: Here you would also send the update to the server
  };

  if (loading) {
    return (
      <div style={{ display: 'grid', gap: '16px', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))' }}>
        {[...Array(3)].map((_, index) => (
          <div key={index} style={{
            backgroundColor: '#F8FAFC',
            borderRadius: '12px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            padding: '16px',
            animation: 'pulse 1.5s infinite',
            height: '100px'
          }} />
        ))}
      </div>
    );
  }

  if (error) {
    return <div style={{ color: '#EF4444' }}>Error: {error}</div>;
  }

  if (tasks.length === 0) {
    return <div style={{ color: '#1E293B' }}>No tasks available. Please add some tasks.</div>;
  }

  return (
    <div style={{ display: 'grid', gap: '16px', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', maxWidth: '1100px', margin: '0 auto' }}>
      {tasks.map(task => (
        <div key={task.id} style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          padding: '24px',
          transition: 'all 0.2s ease',
          cursor: 'pointer',
          outline: 'none'
        }}
        tabIndex={0} 
        aria-label={`Task: ${task.title}, Status: ${task.completed ? 'Completed' : 'Not Completed'}`}
        onClick={() => handleToggleCompletion(task.id)}
        onKeyPress={(e) => e.key === 'Enter' && handleToggleCompletion(task.id)}
        onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
          <h3 style={{ fontWeight: '700', color: '#1E293B' }}>{task.title}</h3>
          <p style={{ fontWeight: '400', color: task.completed ? '#10B981' : '#F59E0B' }}>
            {task.completed ? 'Completed' : 'Not Completed'}
          </p>
        </div>
      ))}
    </div>
  );
};

export default TaskList;