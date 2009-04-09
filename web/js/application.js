
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
		switch ($(this).text()) {
			case 'Upload':
				$('#uploadDialog').dialog('open');
				break;
			case 'Movies':
				reloadTable(getTestMovieJson());
				break;
			case 'Music':
				reloadTable(getTestMusicJson());
				break;
			case 'Software':
				reloadTable(getTestSoftwareJson());
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

	var test = getTestMovieJson();

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

function getTestMovieJson() {
	var rows = [];
	for (i = 0; i < 125; i++) {
		var row = [ '<input type="checkbox" name="download" />', 'Dog Day Afternoon ' + i, 'Drama', 'dogDayAfternoon.avi', '*****', i ];
		rows[i] = row;
	}
	return { 'json' : rows };
}

function getTestMusicJson() {
	var rows = [];
	for (i = 0; i < 125; i++) {
		var row = [ '<input type="checkbox" name="download" />', 'Rancid ' + i, 'Drama', 'rancid.mp3', '*****', i ];
		rows[i] = row;
	}
	return { 'json' : rows };
}

function getTestSoftwareJson() {
	var rows = [];
	for (i = 0; i < 125; i++) {
		var row = [ '<input type="checkbox" name="download" />', 'Ubuntu ' + i, 'Drama', 'ubuntu.tar.gz', '*****', i ];
		rows[i] = row;
	}
	return { 'json' : rows };
}
