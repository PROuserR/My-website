//Process data coming the django template index.html to able to read it in javascript
var tasks_str = String(document.getElementById('tasks').textContent);
var tasks = tasks_str.replace('[', '').replace(']', '');
for (let i = 0; i < tasks.length; i++) {
    tasks = tasks.replace("'", '')
}
tasks = tasks.split(',')


var tasks_date_added_str = String(document.getElementById('tasks_date_added').textContent);
var tasks_date_added = tasks_date_added_str.replace('[', '').replace(']', '');
for (var i = 0; i < tasks_date_added.length; i++) {
    tasks_date_added = tasks_date_added.replace("'", '')
}
tasks_date_added = tasks_date_added.split(',')


var tasks_id_str = String(document.getElementById('tasks_id').textContent);
var tasks_id = tasks_id_str.replace('[', '').replace(']', '');
for (var i = 0; i < tasks_id.length; i++) {
    tasks_id = tasks_id.replace("'", '')
    tasks_id = tasks_id.replace(' ', '')
}
tasks_id = tasks_id.split(',')


var tasks_high_priority_str = String(document.getElementById('tasks_high_priority').textContent);
var tasks_high_priority = tasks_high_priority_str.replace('[', '').replace(']', '');
for (var i = 0; i < tasks_high_priority.length; i++) {
    tasks_high_priority = tasks_high_priority.replace("'", '')
    tasks_high_priority = tasks_high_priority.replace(' ', '')
}
tasks_high_priority = tasks_high_priority.split(',')


var my_events = []
for(var i=0;i < tasks.length;i++)
{
      if (tasks_high_priority[i] == 'True')
      {
        my_events[i] = {
          title: tasks[i],
          start: tasks_date_added[i],
          url: 'http://127.0.0.1:8000/edit_task/' + tasks_id[i],
          backgroundColor: 'red'
      }

      }
      else
      {
        my_events[i] = {
          title: tasks[i],
          start: tasks_date_added[i],
          url: 'http://127.0.0.1:8000/edit_task/' + tasks_id[i],
          backgroundColor: 'blue'
      }
    }

}


document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: [ 'dayGrid', 'timeGrid', 'list', 'bootstrap' ],
    customButtons: {
      newTaskButton: {
        text: 'New Task +',
        click: function() {
          window.location.replace("/new_task/")
        }
      }
    },
    timeZone: 'UTC',
    themeSystem: 'bootstrap',
    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,listMonth'
    },
    footer:{
      right: 'newTaskButton'
    },
    events: my_events
  });

  calendar.render();
});

