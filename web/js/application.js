/**
 * Some globals used throughout the script.
 */
var contentTbl,
    mediaUrl = 'json/';

/**
 * Main method that delegates setting up the page.
 */
function setupUI() {
	setupLayout();
	setupTable();
	setupDownloadDialog();
	setupUploadDialog();
}

/**
 * Uses the fancy jquery.layout plugin to layout the
 * main sections of the page and handles the media events.
 */
function setupLayout() {
	$('body').layout({
		west__showOverflowOnHover : true,
		resizable : false,
		closable : false
	});

	$('.ui-layout-west a').click(function() {
		var txt = $(this).text();
		if (txt == 'Upload') {
		    $('#uploadForm :input').val('');
			$('#errorBox').html('');
			$('#uploadDialog').dialog('open');			
		} else {
			$('.ui-layout-west a').removeClass('selectedCat');
			$(this).addClass('selectedCat');
			getContent(txt);
		}
		return false;
	});

    // Select 'Movies' by default
	$(".ui-layout-west a:contains('Movies')").addClass('selectedCat');
}

/**
 * Creates & populates the table as well as wiring the table row events.
 */
function setupTable() {

    // Clear out the empty rows
    $('tbody').html('');    

	contentTbl = $('#contentTbl').dataTable({
	    bPaginate : true,
	    bLengthChange : false,
		bAutoWidth : false,
		iDisplayLength : 25,
		sPaginationType : 'full_numbers',
		bSortClasses : false,
		bProcessing : true,
		aaSorting : [],
		bStateSave : false,
		sAjaxSource : mediaUrl + 'movies/',
		fnInitComplete : function() { hideAjaxLoader(); },
		oLanguage: {
				sSearch : 'Search:',
				sZeroRecords : 'No files found',
				sInfo : 'Showing _START_ to _END_ of _TOTAL_ files'
		},
		aoColumns : [
		        { bVisible : false, bSearchable : false },
		        { sTitle : 'Title' },
		        { sTitle : 'Newsgroup' },
		        { sTitle : 'Submitted By' },
		        { sTitle : 'Size' },
		        { sTitle : 'Age' }
			]
	});

	setupRowEvents();
	showAjaxLoader();

	// Make the search textbox a little longer and add focus
	$('#contentTbl_filter :text:first').addClass('ui-widget input nzbSearch').attr('size', 50).focus();

	// Add a download btn next to search
	$('#contentTbl_filter').append('&nbsp;<input type="submit" value="Download Selected" id="downloadBtn" class="ui-widget-content nzbBtn" />');

    // Add an event to our download btn
	$('#downloadBtn').click(function() {
	    var selectedRows = getSelectedRows();
	    if (selectedRows.length > 0) {
    		$('#downloadDialog').dialog('open');
    		
    	} else {
    	    $('#invalidDownloadDialog').dialog('open');
    	}
	});
}

/**
 * We use the 'live' methods cause we want to bind the events
 * to the future rows or data.
 */
function setupRowEvents() {

	$('#contentTbl tbody tr').live('mouseover', (function() {
	    if (!$(this).hasClass('selected')) {
	        $(this).addClass('hover');
	    }
	}));

	$('#contentTbl tbody tr').live('mouseout', (function() {
	    if (!$(this).hasClass('selected')) {
	        $(this).removeClass('hover');
	    }
	}));

	$('#contentTbl tbody tr').live('click', (function() {
	    if (!$(this).hasClass('selected')) {
	        $(this).addClass('selected');
	        $(this).removeClass('hover');
	    } else {
	        $(this).removeClass('selected');
	    }
	}));
}

/**
 * Returns an array containing all the selected media ids.
 *
 * @return array - array of primary keys of the selected content
 */
function getSelectedRows() {
    var selectedRows = [],
        tblRows = contentTbl.fnGetNodes(),
        data,
        j = 0;
    for (var i = 0; i < tblRows.length; i++) {
        if ($(tblRows[i]).hasClass('selected')) {
            data = contentTbl.fnGetData(i);
            selectedRows[j] = data[0];
            j++;
        }
    }
    return selectedRows;
}

/**
 * Clears out any selected rows. Called after a download.
 */
function clearSelectedRows() {
    var tblRows = contentTbl.fnGetNodes();
    for (var i = 0; i < tblRows.length; i++) {
        if ($(tblRows[i]).hasClass('selected')) {
            $(tblRows[i]).removeClass('selected');
        }
    }
}

/**
 * Setups our download dialogs.
 */
function setupDownloadDialog() {
	$('#downloadDialog').dialog({
		modal : true,
		autoOpen : false,
		width : '350px',
		title : 'Please enjoy this tasty file',
		buttons : {
			Download : function() {			    
				$(this).dialog('close');
				// TODO: remove the following test alert
				// TODO: pass the server the selected ids
				alert("You would've downloaded the following ids: " + getSelectedRows());
				clearSelectedRows();
			}
		}
	});

	$('#invalidDownloadDialog').dialog({
	    autoOpen : false,
	    modal : true,
	    title : 'Download Fail'
	});
}

/**
 * Setups our upload form dialog and it's validator.
 */
function setupUploadDialog() {

    $('#uploadForm :input').val('');
    $('#size').numeric({ allow : '.' });

	$('#uploadDialog').dialog({
		modal : true,
		autoOpen : false,
		title : 'Thanks for sharing',
		width : '450px',
		buttons : {
			Upload : function() {
		        $('#uploadForm').submit();
		    }
		}
	});

	$('#uploadForm').validate({
	    errorClass : 'important',
	    errorLabelContainer : '#errorBox',
	    wrapper : 'li',
	    rules : {
	        usenet_file : 'required',
	        title : 'required',
	        media : 'required',
	        newsgroup : 'required',
	        size : 'required'
	    },
	    messages : {
	        usenet_file : 'File fail',
	        title : 'Title fail',
	        media : 'Media fail',
	        newsgroup : 'Newsgroup fail',
	        size : 'Size fail'
	    }
	});
}

/**
 * Calls the server for the selected media content & clears
 * the table data & replaces it with the new media data.
 *
 * @param type - Movies, Music or Software
 */
function getContent(type) {
    showAjaxLoader();
    contentTbl.fnClearTable();
	$.getJSON(mediaUrl + type.toLowerCase() + '/', function(data) {
		contentTbl.fnAddData(data.aaData);
		hideAjaxLoader();
	});
}

/**
 * Displays our animated ajax loader image.
 */
function showAjaxLoader() {
    $('#contentTbl_processing').attr('style', 'visibility:visible;').html('<img src="css/images/ajax-loader.gif" alt="Shovelling coal into the server..." />');
}

/**
 * Hides our animated ajax loader image.
 */
function hideAjaxLoader() {
    $('#contentTbl_processing').attr('style', 'visibility:hidden;');
}
