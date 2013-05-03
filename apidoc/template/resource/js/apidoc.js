var conf = {
    version: null,
    scrollMargin: 5
};

function refreshScrollNavigation() {
    $(window).each(function () {
        $(this).scrollspy('refresh');
    });
}

function displayScrollHeader() {
    var scrollHeight = $(document).height(),
        scrollTop = $(window).scrollTop();

    var element = null;
    var items = $(".item:not(#item-head)");
    for (var i = 0, l = items.length; i < l; i++) {
        if ($(items[i]).offset().top >= scrollTop) {
            break;
        }

        element = items[i];
    }

    var header = $("#item-head");
    if (element === null) {
        header.hide();
        return;
    }

    element = $(element);
    var elementTop = element.offset().top;
    if (elementTop > scrollTop || elementTop + element.height() - scrollTop + header.height() - 30 < 0) {
        header.hide();
        return;
    }

    if (header.data('element') != element.attr('id')) {
        $("H4", header).html(element.find("> H4").html());
        $("> .diff-header", header).html(element.find("> .diff-header").html());
        header.removeClass("diff-mode diff-mode-inline diff-mode-side diff-mode-mini diff-mode-full");
        if(element.is(".diff-mode")) {
            header.addClass("diff-mode");
            if(element.is(".diff-mode-side")) {
                header.addClass("diff-mode-side");
            } else {
                header.addClass("diff-mode-inline");
            }
            if(element.is(".diff-mode-full")) {
                header.addClass("diff-mode-full");
            } else {
                header.addClass("diff-mode-mini");
            }
        }

        if (element.data("method") !== undefined) {
            header.attr("data-method", element.data("method"));
        } else {
            header.attr("data-method", null);
        }

        header.data("element", element.attr('id'))
        header.find("> .diff-header > H5").click(function() {
            toggleDiffLayout(element);
        });

        header.find("> .diff-header > .versions > LI").click(function() {
            version = $(this).data("version");
            displayDiff(element, version)
        });

        header.find("> .diff-header > H5 > I.mode-side").click(function(event) {
            event.stopPropagation();
            header.removeClass("diff-mode-side").addClass("diff-mode-inline")
            element.removeClass("diff-mode-side").addClass("diff-mode-inline")
        });
        header.find("> .diff-header > H5 > I.mode-inline").click(function(evente) {
            event.stopPropagation();
            header.removeClass("diff-mode-inline").addClass("diff-mode-side")
            element.removeClass("diff-mode-inline").addClass("diff-mode-side")
        });

        header.find("> .diff-header > H5 > I.mode-full").click(function(event) {
            event.stopPropagation();
            header.removeClass("diff-mode-full").addClass("diff-mode-mini")
            element.removeClass("diff-mode-full").addClass("diff-mode-mini")
        });
        header.find("> .diff-header > H5 > I.mode-mini").click(function(evente) {
            event.stopPropagation();
            header.removeClass("diff-mode-mini").addClass("diff-mode-full")
            element.removeClass("diff-mode-mini").addClass("diff-mode-full")
        });
    }

    header.css({
            width: element.width() + 2,
            top: Math.min(-1, elementTop + element.height() - scrollTop - header.height() - 30)
        })
        .show();

}

function initScrollHeader() {
    $(window).on('scroll resize', displayScrollHeader);
}

function displayVersion() {
    // remember ScrollPosition
    var scrollHeight = $(document).height(),
        scrollTop = $(window).scrollTop();

    var scrollReferenceElement = null;
    var items = $(".item:not(#item-head)");
    for (var i = 0, l = items.length; i < l; i++) {
        if ($(items[i]).offset().top > scrollTop + conf.scrollMargin) {
            break;
        }

        scrollReferenceElement = items[i];

    }

    if (scrollReferenceElement !== null) {
        var offset = $(scrollReferenceElement).offset().top - scrollTop
    }

    $(".method, .type").find(" > .contents > LI").removeClass("active");
    if (conf.version === null) {
        $(".method, .type").find(" > .contents > LI.version:last-child").addClass("active");
    } else {
        $("#nav-versions > LI[data-version].active").removeClass("active");
        $("#nav-versions > LI[data-version=\"" + conf.version + "\"]").addClass("active");

        $(".item > .diff-header > .versions > LI[data-version].active").removeClass("active");
        $(".item > .diff-header > H5.desc").html('<i class="icon-random"></i>' + conf.version)
        $(".item > .diff-header > .versions > LI[data-version=\"" + conf.version + "\"]").addClass("active");
        $(".method, .type").find(" > .contents > LI[data-version~=\"" + conf.version + "\"]").addClass("active");

        $(".diff-mode").each(function() {
            displayDiff($(this))
        });
    }

    if (scrollReferenceElement !== null) {
        $("BODY").scrollTop($(scrollReferenceElement).offset().top - Math.max(offset, 0 - $(scrollReferenceElement).outerHeight() + 60));
        displayScrollHeader();
    }

    refreshScrollNavigation();
}

function hashToParameters(hash)
{
    hash = hash.replace(/^#\/?/, "");
    if (hash === "") {
        return {};
    }

    hash = hash.split("/");
    var parameters = {};
    for (var i = 1, l = hash.length; i < l; i += 2) {
        parameters[hash[i - 1]] = hash[i];
    }

    return parameters;

}

function onNavigationChange() {
    var parameters = hashToParameters(window.location.hash);

    if (parameters === {}) {
        return;
    }

    if (parameters.version) {
        if (conf.version != parameters.version) {
            conf.version = parameters.version;
            displayVersion(parameters.version);
        }
    }

    elementSelector = null;
    if (parameters.section) {
        if (parameters.method) {
            elementSelector = "#m-" + parameters.section + "-" + parameters.method;
        } else {
            elementSelector = "#s-" + parameters.section;
        }
    } else if (parameters.namespace) {
        if (parameters.type) {
            elementSelector = "#t-" + parameters.type;
        } else {
            elementSelector = "#n-" + parameters.namespace;
        }
    } else if (parameters.type) {
        elementSelector = "#t-" + parameters.type;
    }

    if (elementSelector !== null && $(elementSelector).length) {
        $("BODY").scrollTop($(elementSelector).offset().top - conf.scrollMargin);
    }
}

function navigateTo(newParameters, removeParameters) {
    var parameters = hashToParameters(window.location.hash);
    if (removeParameters !== null) {
        for (var j = 0, l = removeParameters.length; j < l; j++) {
            delete parameters[removeParameters[j]];
        }
    }

    for (var i in newParameters) {
        parameters[i] = newParameters[i];
    }


    var hash = "#";
    for (i in parameters) {
        hash += "/" + i + "/" + parameters[i];
    }

    if (window.location.hash == hash) {
        onNavigationChange();
    } else {
        window.location.href = hash;
    }
}

function initNavigation() {
    var firstVersion = $("#nav-versions > LI[data-version][data-status=CURRENT]");
    if (firstVersion.length === 0) {
        firstVersion = $("#nav-versions > LI[data-version]");
    }

    if (firstVersion.length === 0) {
        conf.version = null;
    } else {
        conf.version = firstVersion.first().data("version");
    }

    $(window).bind("hashchange", onNavigationChange);

    displayVersion();
}

function focusNavigation() {
    if (!window.matchMedia('(max-width: 767px)').matches) {
        var target = $(".scroll-spyable .active");
        var container = $(".doc-sidebar");
        var relativeTop = target.offset().top - container.offset().top;
        if (relativeTop < 0) {
            container.scrollTop(container.scrollTop() + relativeTop -  conf.scrollMargin);
        } else if (relativeTop + target.outerHeight() > container.outerHeight()) {
            container.scrollTop(container.scrollTop() + (relativeTop + target.outerHeight() - container.outerHeight()) + conf.scrollMargin);
        }
    }
}

function initScrollNavigation() {
    $(window).scrollspy({target: '.scroll-spyable'});
    $('.doc-sidebar').affix({
        offset: {
            top: 40
        }
    });

    $('.scroll-spyable').on('activate', function (e) {
        focusNavigation();
    });
    $(window).on('resize', refreshScrollNavigation);
}

function escapeRegExp(str) {
    return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
}


function initSearch() {
    var toSearch = 0;
    var lastSearch = null;
    var groupsElements = $(".doc-sidenav>LI[data-group]:not([data-item])");

    $("[type=search]").bind('change keyup keypress search', function (event) {
        if (event.keyCode == 13) {
            $(this).blur();
        }
        clearTimeout(toSearch);
        search = $(this).val().toLowerCase().replace(/\s+/g, ' ').replace(/(^\s+|\s+$)/, '');
        if (search === "") {
            groupsElements.show();
            groupsElements.each(function () {
                groupElement = $(this);
                groupElement.find('H6').html(groupElement.data("group"));
            });

            var itemsElements = $(".doc-sidenav>LI[data-group][data-item]");
            itemsElements.show();
            itemsElements.each(function (itemElement) {
                itemElement = $(this);
                itemElement.find('>A>SPAN').html(itemElement.data("item"));
            });

            return;
        }
        toSearch = setTimeout(function () {
            if (search === lastSearch) {
                return;
            }

            lastSearch = search;

            var words = escapeRegExp(search).split(/\s/);
            var wordsReg = new RegExp("(" + words.join("|") + ")", 'gi');
            for (var i=0, l=groupsElements.length; i<l; i++) {
                var groupElement = $(groupsElements[i]);
                var groupName = groupElement.data("group");
                var matchGroup = wordsReg.test(groupName);

                var itemsElements = $(".doc-sidenav>LI[data-group=" + groupName + "][data-item]");
                var matchOneitem = false;
                for (var k=0, n=itemsElements.length; k<n; k++) {
                    var itemElement = $(itemsElements[k]);
                    var itemName = itemElement.data("item");
                    var matchItem = wordsReg.test(itemName);
                    if (matchItem) {
                        matchOneitem = true;
                    }

                    if (matchItem) {
                        itemElement.find('A>SPAN').html(itemName.replace(wordsReg, '<span class="highlight">$1</span>'));
                        itemElement.show();
                    } else {
                        itemElement.find('A>SPAN').html(itemName);
                        itemElement.hide();
                    }
                }

                if (matchGroup || matchOneitem) {
                    groupElement.find('H6').html(groupName.replace(wordsReg, '<span class="highlight">$1</span>'));
                    groupElement.show();
                    if (matchGroup && !matchOneitem) {
                        itemsElements.show();
                    }
                } else {
                    groupElement.hide();
                    itemsElements.hide();
                }
            }

        }, 20);
    });
}


function displayDiff(item, version) {
    if (version==null) {
        version = $("#nav-versions > LI[data-version]:not([data-version~=\"" + conf.version + "\"])").first().data("version");
    }
    item.find(" > .diff-header > .versions > LI").removeClass("diff_left diff_right")
    item.find(" > .diff-header > .versions > LI[data-version~=\"" + conf.version + "\"]").addClass("diff_left")
    item.find(" > .diff-header > .versions > LI[data-version~=\"" + version + "\"]").addClass("diff_right")
    if ($("#item-head").data('element') == item.attr("id")) {
        $("#item-head > .diff-header > .versions > LI").removeClass("diff_left diff_right")
        $("#item-head > .diff-header > .versions > LI[data-version~=\"" + conf.version + "\"]").addClass("diff_left")
        $("#item-head > .diff-header > .versions > LI[data-version~=\"" + version + "\"]").addClass("diff_right")
    }

    item.find(" > .contents > LI.diff-left > H5.title").text(conf.version)
    item.find(" > .contents > LI.diff-right > H5.title").text(version)
    item.find(" > .contents > LI.diff .diff_version").show().removeClass("diff_new diff_del")
    item.find(" > .contents > LI.diff .diff_version:not([data-version~=\"" + conf.version + "\"]):not([data-version~=\"" + version + "\"])").hide()
    item.find(" > .contents > LI.diff .diff_version[data-version~=\"" + version + "\"]:not([data-version~=\"" + conf.version + "\"])").addClass("diff_new")
    item.find(" > .contents > LI.diff .diff_version[data-version~=\"" + conf.version + "\"]:not([data-version~=\"" + version + "\"])").addClass("diff_del")

    refreshScrollNavigation()
}

function toggleDiffLayout(item) {
    item.toggleClass("diff-mode");
    if (item.is(".diff-mode")) {
        item.addClass("diff-mode-side").removeClass("diff-mode-inline");
        item.addClass("diff-mode-full").removeClass("diff-mode-mini");
        if ($("#item-head").data('element') == item.attr("id")) {
            $("#item-head").addClass("diff-mode diff-mode-side").removeClass("diff-mode-inline");
            $("#item-head").addClass("diff-mode diff-mode-full").removeClass("diff-mode-mini");
        }

        displayDiff(item)

        if (item.offset().top + item.outerHeight() - 60 < $("BODY").scrollTop()) {
            $("BODY").scrollTop(item.offset().top + item.outerHeight() - 60);
        }
    } else {
        item.removeClass("diff-mode diff-mode-side diff-mode-inline diff-mode-full diff-mode-mini");
        if ($("#item-head").data('element') == item.attr("id")) {
            $("#item-head").removeClass("diff-mode diff-mode-side diff-mode-inline diff-mode-full diff-mode-mini");
        }

        item.find(" > .contents > LI.version[data-version~=\"" + conf.version + "\"]").addClass("active");

        refreshScrollNavigation()
    }
}

function initDiff() {
    $(".item>.diff-header > H5").click(function() {
        item = $(this).closest(".item");
        toggleDiffLayout(item);

    });
    $(".item>.diff-header > H5 > I.mode-side").click(function(event) {
        event.stopPropagation();
        item = $(this).closest(".item");
        item.removeClass("diff-mode-side").addClass("diff-mode-inline")
    });
    $(".item>.diff-header > H5 > I.mode-inline").click(function(evente) {
        event.stopPropagation();
        item = $(this).closest(".item");
        item.removeClass("diff-mode-inline").addClass("diff-mode-side")
    });
    $(".item>.diff-header > H5 > I.mode-full").click(function(event) {
        event.stopPropagation();
        item = $(this).closest(".item");
        item.removeClass("diff-mode-full").addClass("diff-mode-mini")
    });
    $(".item>.diff-header > H5 > I.mode-mini").click(function(evente) {
        event.stopPropagation();
        item = $(this).closest(".item");
        item.removeClass("diff-mode-mini").addClass("diff-mode-full")
    });

    $(".item>.diff-header > .versions > LI").click(function() {
        item = $(this).closest(".item");
        version = $(this).data("version");
        displayDiff(item, version)

    });

    $(".item > .contents > .diff").each(function() {
        $(this).addClass("diff-left").clone().insertAfter($(this)).addClass("diff-right").removeClass("diff-left");
    })
}

function shortcutSearch(event, key) {
    if (event.preventDefault) {
        event.preventDefault();
    } else {
        // internet explorer
        event.returnValue = false;
    }
    console.log(arguments)
    $("[type=search]").select();
}

function shortcutGotoNext(event, key) {
    var current = $(".scroll-spyable>UL>LI.active:visible")
    if (current.length == 0) {
        $(".scroll-spyable>UL>LI[data-item]:visible>A").get(0).click()
    } else {
        var items = current.nextAll("LI[data-item]:visible").find(">A");
        if (items.length > 0) {
            items.get(0).click()
        } else {
            var ul = current.closest("UL");
            var itemsInNextGroup = current.closest("UL").next().find('>LI[data-item]:visible>A')
            if (itemsInNextGroup.length > 0) {
                itemsInNextGroup.get(0).click();
            }
        }
    }
}

function shortcutGotoPrevious(event, key) {
    var current = $(".scroll-spyable>UL>LI.active:visible")
    if (current.length == 0) {
        $(".scroll-spyable>UL>LI[data-item]:visible>A").get(0).click()
    } else {
        var items = current.prevAll("LI[data-item]:visible").find(">A");
        if (items.length > 0) {
            items.get(items.length - 1).click()
        } else {
            var ul = current.closest("UL");
            var itemsInPrevGroup = current.closest("UL").prev().find('>LI[data-item]:visible>A')
            if (itemsInPrevGroup.length > 0) {
                itemsInPrevGroup.get(itemsInPrevGroup.length - 1).click();
            }
        }
    }
}

function shortcutGotoNextVersion(event, key) {
    var current = $("#nav-versions>LI.active:visible")
    if (current.length == 0) {
        $("#nav-versions>LI[data-version]:visible>A").get(0).click()
    } else {
        var items = current.nextAll("LI[data-version]:visible").find(">A");
        if (items.length > 0) {
            items.get(0).click()
        }
    }
}

function shortcutGotoPreviousVersion(event, key) {
    var current = $("#nav-versions>LI.active:visible")
    if (current.length == 0) {
        $("#nav-versions>LI[data-version]:visible>A").get(0).click()
    } else {
        var items = current.prevAll("LI[data-version]:visible").find(">A");
        if (items.length > 0) {
            items.get(items.length - 1).click()
        }
    }
}

function shortcutHelp(event, key) {
    $(".help_popup, .help_overlay").show()
    Mousetrap.bind('esc', shortcutHelpHide)
}

function shortcutHelpHide(event, key) {
    $(".help_popup, .help_overlay").hide()
    Mousetrap.unbind('esc', shortcutHelpHide)
}

function initShortcuts() {
    Mousetrap.bind('?', shortcutHelp);
    Mousetrap.bind('/', shortcutSearch);
    Mousetrap.bind(['n', 'j'], shortcutGotoNext);
    Mousetrap.bind(['p', 'k'], shortcutGotoPrevious);
    Mousetrap.bind(['v'], shortcutGotoNextVersion);
    Mousetrap.bind(['c'], shortcutGotoPreviousVersion);
}

function initHelp() {
    $(".help_overlay").click(shortcutHelpHide)
}

$(document).ready(function () {
    initScrollNavigation();
    initScrollHeader();
    initNavigation();
    initDiff();
    initSearch();
    initShortcuts();
    initHelp();

    onNavigationChange();
});

