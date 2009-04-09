
function setupUI() {
	setupLayout();
	setupTable();
	setupDownloadDialog();
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
		if (txt == 'Upload') {
			$('#uploadDialog').dialog('open');
		} else {
			reloadTable(getTestJson(txt));
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
		bSortClasses : false,
		aaSorting : [],
		aaData : test.json,
		aoColumns : [
		        { bVisible : false, bSearchable : false },
				{ bSearchable : false, sTitle : 'Download' },
		        { sTitle : 'Title' },
		        { sTitle : 'Genre' },
		        { sTitle : 'Filename' },
		        { sTitle : 'Rating' },
		        { sTitle : 'Days Active' }
			],
		fnRowCallback : function(nRow, aData, iDisplayIndex) {
			var cssClass = nRow.className;
			nRow.onmouseover = function() { nRow.className = 'hover'; };
			nRow.onmouseout = function() { nRow.className = cssClass; };
			nRow.onclick = function() {
				alert('You click on content id: ' + aData[0]);
			};

			return nRow;
		}
	});

	// Make the search textbox a little longer
	$('#contentTbl_filter :text:first').attr('size', 50);

	// Add a download btn next to search
	$('#contentTbl_filter').append('&nbsp;<input type="submit" value="Download Selected" id="downloadBtn" class="ui-widget-content" />');

	$('#downloadBtn').click(function() {
		$('#downloadDialog').dialog('open');
	});
}

function setupDownloadDialog() {
	$('#downloadDialog').dialog({
		modal : true,
		autoOpen : false,
		width : '350px',
		buttons : {
			Close : function() {
				$(this).dialog('close');
			}
		}
	});
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
		default:
			title = 'Unknown';
			filename = 'unknown.txt';
	}
	for (i = 0; i < 125; i++) {
		// Data in index 0 is suppose to represent the id of the content
		var id = 'content-' + i;
		rows[i] = [ i, '<input type="checkbox" name="download" id="'+id+'" />', title, type, filename, '*****', i ];
	}
	return { 'json' : rows };
}
