//Process data coming the django template index.html to able to read it in javascript
var weekly_tasks_str = String(document.getElementById('weekly_tasks').textContent);
var weekly_tasks = weekly_tasks_str.replace('[', '').replace(']', '');
for (let i = 0; i < weekly_tasks.length; i++) {
    weekly_tasks = weekly_tasks.replace("'", '')
}
weekly_tasks = weekly_tasks.split(',')


var weekly_tasks_date_added_str = String(document.getElementById('weekly_tasks_date_added').textContent);
var weekly_tasks_date_added = weekly_tasks_date_added_str.replace('[', '').replace(']', '');
for (var i = 0; i < weekly_tasks_date_added.length; i++) {
    weekly_tasks_date_added = weekly_tasks_date_added.replace("'", '')
}
weekly_tasks_date_added = weekly_tasks_date_added.split(',')


var weekly_tasks_id_str = String(document.getElementById('weekly_tasks_id').textContent);
var weekly_tasks_id = weekly_tasks_id_str.replace('[', '').replace(']', '');
for (var i = 0; i < weekly_tasks_id.length; i++) {
    weekly_tasks_id = weekly_tasks_id.replace("'", '')
    weekly_tasks_id = weekly_tasks_id.replace(' ', '')
}
weekly_tasks_id = weekly_tasks_id.split(',')


var weekly_tasks_high_priority_str = String(document.getElementById('weekly_tasks_high_priority').textContent);
var weekly_tasks_high_priority = weekly_tasks_high_priority_str.replace('[', '').replace(']', '');
for (var i = 0; i < weekly_tasks_high_priority.length; i++) {
    weekly_tasks_high_priority = weekly_tasks_high_priority.replace("'", '')
    weekly_tasks_high_priority = weekly_tasks_high_priority.replace(' ', '')
}
weekly_tasks_high_priority = weekly_tasks_high_priority.split(',')


var my_events = []
for(var i=0;i < weekly_tasks.length;i++)
{
      if (weekly_tasks_high_priority[i] == 'True')
      {
        my_events[i] = {
          title: weekly_tasks[i],
          start: weekly_tasks_date_added[i],
          url: 'edit_task/' + weekly_tasks_id[i],
          backgroundColor: 'red'
      }

      }
      else
      {
        my_events[i] = {
          title: weekly_tasks[i],
          start: weekly_tasks_date_added[i],
          url: 'edit_task/' + weekly_tasks_id[i],
          backgroundColor: 'blue'
      }
    }

}


document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: [ 'dayGrid', 'timeGrid', 'list', 'bootstrap' ],
    timeZone: 'UTC',
    themeSystem: 'bootstrap',
    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
    },
    events: my_events
  });

  calendar.render();
});