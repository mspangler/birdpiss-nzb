
function setupUI() {
	setupLayout();
	setupTable();
	setupUploadDialog();
}

function setupLayout() {
	$('body').layout({
		west__showOverflowOnHover : true,
		resizable : false,
		closable : false
	});

	$('.ui-layout-west a').click(function() {
		var txt = $(this).text();
		switch (txt) {
			case 'Upload':
				$('#uploadDialog').dialog('open');
				break;
			default:
				reloadTable(getTestJson(txt));
				break;
		}
		return false;
	});
}

function reloadTable(data) {
	if (contentTbl) {
		contentTbl.fnClearTable();
		contentTbl.fnAddData(data.json);
	}
}

var contentTbl;
function setupTable() {

	var test = getTestJson('Movies');

	contentTbl = $('#contentTbl').dataTable({
	    bPaginate : true,
	    bLengthChange : false,
		bAutoWidth : false,
		iDisplayLength : 10,
		sPaginationType : 'full_numbers',
		aaData : test.json,
		aoColumns : [
				{ sTitle : 'Download' },
		        { sTitle : 'Title' },
		        { sTitle : 'Genre' },
		        { sTitle : 'Filename' },
		        { sTitle : 'Rating' },
		        { sTitle : 'Days Active' }
			]
	});

	// Make the search textbox a little longer
	$('#contentTbl_filter :text:first').attr('size', 50);

	// Add a download btn next to search
	$('#contentTbl_filter').append('&nbsp;<input type="submit" value="Download Selected" class="ui-widget-content" />');
}

function setupUploadDialog() {
	$('#uploadDialog').dialog({
		modal : true,
		autoOpen : false,
		width : '400px',
		buttons : {
			Close : function() {
				$(this).dialog('close');
			}
		}
	});
}

function getTestJson(type) {
	var rows = [], title, filename;
	switch (type) {
		case 'Movies':
			title = 'Dog Day Afternoon'
			filename = 'dogDayAfternoon.avi'
			break;
		case 'Music':
			title = 'Rancid'
			filename = 'rancid.mp3'
			break;
		case 'Software':
			title = 'Ubuntu'
			filename = 'ubuntu.tar.gz'
			break;
	}
	for (i = 0; i < 125; i++) {
		var row = [ '<input type="checkbox" name="download" />', title, type, filename, '*****', i ];
		rows[i] = row;
	}
	return { 'json' : rows };
}
