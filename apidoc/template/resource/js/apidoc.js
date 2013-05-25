var conf = {
    version: null,
    multiVersion: false,
    scrollMargin: 5
};

function refreshScrollNavigation() {
    setTimeout(function() {
        $(window).each(function () {
            $(this).scrollspy('refresh');
        });
    }, 100);
}

function getCurrentItem() {
    var scrollTop = $(window).scrollTop();

    var items = $(".item:not(#item-head)");

    var dic = function(inf, sup) {
        if (sup < 0) {
            return null;
        }

        if (sup <= inf) {
            return items[sup];
        }

        var index = inf + Math.round((sup - inf)/2);
        var item = $(items[index]);
        if (item.offset().top >= scrollTop) {
            return dic(inf, index - 1);
        }

        if (item.offset().top + item.outerHeight() >= scrollTop) {
            return items[index];
        }

        return dic(index + 1, sup)
    }

    return dic(0, items.length - 1);

}

function displayScrollHeader() {
    var scrollHeight = $(document).height(),
        scrollTop = $(window).scrollTop();

    var element = getCurrentItem();

    var header = $("#item-head");
    if (element === null) {
        header.hide();
        return;
    }

    element = $(element);

    var subElement = null;
    var items = $(".stack H5:visible", element);
    items.sort(function(a, b) {
        var at = $(a).offset().top;
        var bt = $(b).offset().top;
        if (at < bt) return -1;
        if (at > bt) return 1;
        return 0;
    });

    header.find(".stack").hide()
    var subScrollTop = scrollTop + header.outerHeight();
    for (var i = 0, l = items.length; i < l; i++) {
        var pos = $(items[i]).offset().top - subScrollTop
        if (pos > 0) {
            if (pos < 30) {
                subElement = null;
            }

            break;
        }

        subElement = items[i];
    }

    if (subElement === null) {
    } else {
        header.find(".stack").html("<h5>" + $(subElement).html() + "</h5>").show()
    }


    var elementTop = element.offset().top;
    if (elementTop > scrollTop || elementTop + element.height() - scrollTop + header.height() - 30 < 0) {
        header.hide();
        return;
    }

    if (header.data('element') != element.attr('id')) {
        if (header.data('element') !== null) {
            $("#" + header.data('element')).unbind("headerChanged")
        }

        header.data("element", element.attr('id'))

        if (element.data("method") !== undefined) {
            header.attr("data-method", element.data("method"));
        } else {
            header.attr("data-method", null);
        }

        $("H4", header).html(element.find("> H4").html());
        $("> .diff-header", header).html(element.find("> .diff-header").html());

        $(".mode-side, .mode-inline", header).attr("title", "Toggle side by side / inline mode").tooltip({placement:"bottom"})
        $(".mode-full, .mode-mini", header).attr("title", "Toggle full / strict diff").tooltip({placement:"bottom"})

        header.find("> .diff-header > H5").click(function() {
            toggleDiffLayout(element);
        });
        header.find("> .diff-header > .versions > LI").click(function() {
            displayDiff(element, $(this).data("version"))
        });
        header.find("> .diff-header > H5 > I.mode-side").click(function(event) {
            event.stopPropagation();
            diffActivateModeInline(element);
        });
        header.find("> .diff-header > H5 > I.mode-inline").click(function(evente) {
            event.stopPropagation();
            diffActivateModeSide(element);
        });
        header.find("> .diff-header > H5 > I.mode-full").click(function(event) {
            event.stopPropagation();
            diffActivateModeMini(element);
        });
        header.find("> .diff-header > H5 > I.mode-mini").click(function(evente) {
            event.stopPropagation();
            diffActivateModeFull(element);
        });

        element.bind("headerChanged", function() {
            element = $(this)
            header.removeClass("diff-mode diff-mode-inline diff-mode-side diff-mode-mini diff-mode-full");
            header.find(" > .diff-header > .versions > LI").removeClass("diff_left diff_right")

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

            header.find(" > .diff-header > .versions > LI:eq(" + element.find(" > .diff-header > .versions > LI.diff_left").index() + ")").addClass("diff_left");
            header.find(" > .diff-header > .versions > LI:eq(" + element.find(" > .diff-header > .versions > LI.diff_right").index() + ")").addClass("diff_right");
        });
        element.trigger("headerChanged");
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

    $(".item > .contents > .sample > :not([data-version~=\"" + conf.version + "\"])").hide();
    if (conf.version !== null) {
        $("#nav-versions > LI[data-version].active").removeClass("active");
        $("#nav-versions > LI[data-version=\"" + conf.version + "\"]").addClass("active");

        $(".item > .diff-header > H5.desc").html('<i class="i-diff"></i>' + conf.version)
        $(".item, .nav-list > LI").attr("data-changed", null)

        $(".item > .diff-header > .versions > LI:not(:first-child):not([data-changed=none])[data-version=\"" + conf.version + "\"]").each(function() {
            var item = $(this).closest(".item");
            var status = $(this).data("changed");
            item.attr("data-changed", status)
            $(".nav-list > LI > A[data-target=\"#" + item.attr("id") + "\"]").closest("LI").attr("data-changed", status)
        })

        $(".item > .contents > .sample > [data-version~=\"" + conf.version + "\"]").show();
        $(".item > .contents .diff_version").removeClass("diff_new diff_del diff_none");
        $(".item > .contents .diff_version[data-version~=\"" + conf.version + "\"]").addClass("diff_new")

        $(".diff-mode").each(function() {
            displayDiff($(this))
        });
    } else {
        $(".item > .contents > .sample > [data-version]").show();
        $(".item > .contents .diff_version").removeClass("diff_new diff_del diff_none");
        $(".item > .contents .diff_version").addClass("diff_new")
    }

    if (scrollReferenceElement !== null) {
        $(window).scrollTop($(scrollReferenceElement).offset().top - Math.max(offset, 0 - $(scrollReferenceElement).outerHeight() + 60));
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
    if (parameters.method) {
        elementSelector = "#m-" + parameters.method;
    } else if (parameters.type) {
        elementSelector = "#t-" + parameters.type;
    } else if (parameters.category) {
        elementSelector = "#c-" + parameters.category;
    }

    if (elementSelector !== null && $(elementSelector).length) {
        $(window).scrollTop($(elementSelector).offset().top - conf.scrollMargin);
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
        conf.multiVersion = false;
    } else {
        conf.version = firstVersion.first().data("version");
        conf.multiVersion = true;
    }

    $(window).bind("hashchange", onNavigationChange);

    displayVersion();
}

function focusNavigation() {
    if (!window.matchMedia('(max-width: 767px)').matches) {
        // pas de focus si la souris est sur la navigation
        if ($(".doc-sidebar").data('hover')) {
            return;
        }
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
            top: $(".container").outerHeight()
        }
    });

    $('.scroll-spyable').on('activate', function (e) {
        focusNavigation();
    });
    $(window).on('resize', refreshScrollNavigation);
    $(".doc-sidebar").hover(
        function() { $.data(this, 'hover', true); },
        function() { $.data(this, 'hover', false); }
    ).data('hover', false);

    // On peut, du coup, vérifier à chaque fois si la souris est sur l'élément

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
        var lastVersion = item.find(".diff_second");
        if (lastVersion.length > 0) {
            version = lastVersion.data("version");
        } else {
            version = $("#nav-versions > LI[data-version]:not([data-version~=\"" + conf.version + "\"])").first().data("version");
        }
    }

    var firstIndex = $("#nav-versions > LI[data-version~=\"" + conf.version + "\"]").index()
    var secondIndex = $("#nav-versions > LI[data-version~=\"" + version + "\"]").index()

    if (firstIndex < secondIndex) {
        leftVersion = conf.version
        rightVersion = version
    } else {
        leftVersion = version
        rightVersion = conf.version
    }

    item.find(" > .diff-header > .versions > LI").removeClass("diff_second diff_first diff_left diff_right")
    item.find(" > .diff-header > .versions > LI[data-version~=\"" + conf.version + "\"]").addClass("diff_first")
    item.find(" > .diff-header > .versions > LI[data-version~=\"" + version + "\"]").addClass("diff_second")
    item.find(" > .diff-header > .versions > LI[data-version~=\"" + leftVersion + "\"]").addClass("diff_left")
    item.find(" > .diff-header > .versions > LI[data-version~=\"" + rightVersion + "\"]").addClass("diff_right")

    item.trigger("headerChanged");

    item.find(" > .contents.content-left > H5.title").text(leftVersion)
    item.find(" > .contents.content-right > H5.title").text(rightVersion)
    item.find(" > .contents .diff_version").removeClass("diff_new diff_del diff_none")
    item.find(" > .contents .diff_version:not([data-version~=\"" + rightVersion + "\"]):not([data-version~=\"" + leftVersion + "\"])").addClass("diff_none")
    item.find(" > .contents .diff_version[data-version~=\"" + rightVersion + "\"]:not([data-version~=\"" + leftVersion + "\"])").addClass("diff_new")
    item.find(" > .contents .diff_version[data-version~=\"" + leftVersion + "\"]:not([data-version~=\"" + rightVersion + "\"])").addClass("diff_del")

    refreshScrollNavigation()
}

function toggleDiffLayout(item) {
    item.toggleClass("diff-mode");
    if (item.is(".diff-mode")) {
        item.addClass("diff-mode-side").removeClass("diff-mode-inline");
        item.addClass("diff-mode-full").removeClass("diff-mode-mini");

        displayDiff(item)

        keepFocusOnItem(item);
    } else {
        item.removeClass("diff-mode diff-mode-side diff-mode-inline diff-mode-full diff-mode-mini");

        item.find(" > .contents .diff_version").removeClass("diff_new diff_del diff_none")
        item.find(" > .contents .diff_version[data-version~=\"" + conf.version + "\"]").addClass("diff_new")

        item.trigger("headerChanged");

        refreshScrollNavigation()
    }
}

function diffActivateModeInline(item) {
    item.removeClass("diff-mode-side").addClass("diff-mode-inline")
    item.trigger("headerChanged");

    keepFocusOnItem(item);
}

function diffActivateModeSide(item) {
    item.removeClass("diff-mode-inline").addClass("diff-mode-side")
    item.trigger("headerChanged");

    keepFocusOnItem(item);
}

function diffActivateModeFull(item) {
    item.removeClass("diff-mode-mini").addClass("diff-mode-full")
    item.trigger("headerChanged");

    keepFocusOnItem(item);
}

function diffActivateModeMini(item) {
    item.removeClass("diff-mode-full").addClass("diff-mode-mini")
    item.trigger("headerChanged");

    keepFocusOnItem(item);
}

function keepFocusOnItem(item) {
    if (item.offset().top + item.outerHeight() - 60 < $(window).scrollTop()) {
        $(window).scrollTop(item.offset().top + item.outerHeight() - 100);
    }
}

function initDiff() {
    $(".item>.diff-header > H5").click(function() {
        item = $(this).closest(".item");
        toggleDiffLayout(item);

    });
    $(".item>.diff-header > H5 > I.mode-side").click(function(event) {
        event.stopPropagation();
        diffActivateModeInline($(this).closest(".item"));
    });
    $(".item>.diff-header > H5 > I.mode-inline").click(function(evente) {
        event.stopPropagation();
        diffActivateModeSide($(this).closest(".item"));
    });
    $(".item>.diff-header > H5 > I.mode-full").click(function(event) {
        event.stopPropagation();
        diffActivateModeMini($(this).closest(".item"));
    });
    $(".item>.diff-header > H5 > I.mode-mini").click(function(evente) {
        event.stopPropagation();
        diffActivateModeFull($(this).closest(".item"));
    });
    $(".item>.diff-header > .versions > LI").click(function() {
        displayDiff($(this).closest(".item"), $(this).data("version"))
    });
    $(".item > .contents").each(function() {
        $(this).addClass("content-left").clone().insertAfter($(this)).addClass("content-right").removeClass("content-left").find("> .sample").remove();
    });

    $(".mode-side, .mode-inline").attr("title", "Toggle side by side / inline mode").tooltip({placement:"bottom"})
    $(".mode-full, .mode-mini").attr("title", "Toggle full / strict diff").tooltip({placement:"bottom"})
}

function shortcutSearch(event, key) {
    if (event.preventDefault) {
        event.preventDefault();
    } else {
        // internet explorer
        event.returnValue = false;
    }
    $("[type=search]").select();
}

function shortcutGotoPrevious(event, key) {
    var current = $(".scroll-spyable>UL>LI.active:visible")
    if (current.length == 0) {
        $(".scroll-spyable>UL>LI[data-item]:visible>A").get(0).click()
    } else {
        var items = current.prevAll("LI[data-item]:visible").find(">A");
        if (items.length > 0) {
            items.sort(function(a, b) {
                if ($(a).index() < $(b).index()) return 1;
                if ($(a).index() > $(b).index()) return -1;
                return 0;
            });
            items.get(items.length - 1).click()
        } else {
            var ul = current.closest("UL");
            var itemsInPrevGroup = current.closest("UL").prev().find('>LI[data-item]:visible>A')
            if (itemsInPrevGroup.length > 0) {
                itemsInPrevGroup.last().get(0).click();
            }
        }
    }
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

function shortcutGotoPreviousVersion(event, key) {
    var current = $("#nav-versions>LI.active:visible")
    if (current.length == 0) {
        $("#nav-versions>LI[data-version]:visible>A").get(0).click()
    } else {
        var items = current.prevAll("LI[data-version]:visible");
        if (items.length > 0) {
            items.sort(function(a, b) {
                if ($(a).index() < $(b).index()) return 1;
                if ($(a).index() > $(b).index()) return -1;
                return 0;
            });
            items.first().find(">A").get(0).click()
        }
    }
}

function shortcutGotoNextVersion(event, key) {
    var current = $("#nav-versions>LI.active:visible")
    if (current.length == 0) {
        $("#nav-versions>LI[data-version]:visible>A").get(0).click()
    } else {
        var items = current.nextAll("LI[data-version]:visible");
        if (items.length > 0) {
            items.sort(function(a, b) {
                if ($(a).index() < $(b).index()) return -1;
                if ($(a).index() > $(b).index()) return 1;
                return 0;
            });
            items.first().find(">A").get(0).click()
        }
    }
}

function getActiveItem() {
    var current = $(".scroll-spyable>UL>LI.active:visible[data-item]>A")
    if (current.length == 0) {
        var currentActive = $(".scroll-spyable>UL>LI.active:visible")
        if (currentActive.length == 0) {
            current = $(".scroll-spyable>UL>LI[data-item]:visible>A");
        } else {
            current = currentActive.nextAll("LI[data-item]:visible").find(">A");
            if (current.length == 0) {
                var ul = current.closest("UL");
                var current = current.closest("UL").next().find('>LI[data-item]:visible>A')
            }
        }

        if (current.length > 0) {
            current.get(0).click()
        }
    }
    return current.first();
}
function shortcutToggleDiff(event, key) {
    current = getActiveItem();

    if (current.length > 0) {
        toggleDiffLayout($(current.data('target')))
    }
}

function shortcutToggleSide(event, key) {
    var current = getActiveItem();

    if (current.length > 0) {
        var element = $(current.data('target'))
        if (!element.is(".diff-mode")) {
            toggleDiffLayout($(current.data('target')))
            diffActivateModeInline(element);
            return;
        }

        if ($(current.data('target')).is(".diff-mode-side")) {
            diffActivateModeInline(element);
        } else {
            diffActivateModeSide(element);
        }
    }
}

function shortcutToggleFull(event, key) {
    var current = getActiveItem();

    if (current.length > 0) {
        var element = $(current.data('target'))
        if (!element.is(".diff-mode")) {
            toggleDiffLayout($(current.data('target')))
            diffActivateModeMini(element);
            return;
        }

        if ($(current.data('target')).is(".diff-mode-mini")) {
            diffActivateModeFull(element);
        } else {
            diffActivateModeMini(element);
        }
    }
}

function shortcutGotoNextDiffVersion(event, key) {
    var current = getActiveItem();

    if (current.length > 0) {
        var element = $(current.data('target'))
        if (!element.is(".diff-mode")) {
            toggleDiffLayout($(current.data('target')))
        }

        var current = element.find(".diff_second");
        if (current.length > 0) {
            var items = current.nextAll("LI[data-version]:visible");
            if (items.length > 0) {
                items.sort(function(a, b) {
                    if ($(a).index() < $(b).index()) return -1;
                    if ($(a).index() > $(b).index()) return 1;
                    return 0;
                })
                items.get(0).click()
            }
        }
    }
}

function shortcutGotoPreviousDiffVersion(event, key) {
    var current = getActiveItem();

    if (current.length > 0) {
        var element = $(current.data('target'))
        if (!element.is(".diff-mode")) {
            toggleDiffLayout($(current.data('target')))
        }

        var current = element.find(".diff_second");
        if (current.length > 0) {
            var items = current.prevAll("LI[data-version]:visible");
            if (items.length > 0) {
                items.sort(function(a, b) {
                    if ($(a).index() < $(b).index()) return 1;
                    if ($(a).index() > $(b).index()) return -1;
                    return 0;
                })
                items.get(0).click()
            }
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
    Mousetrap.bind(['p', 'k'], shortcutGotoPrevious);
    Mousetrap.bind(['n', 'j'], shortcutGotoNext);

    if (conf.multiVersion) {
        Mousetrap.bind(['b'], shortcutGotoPreviousVersion);
        Mousetrap.bind(['v'], shortcutGotoNextVersion);
        Mousetrap.bind(['d'], shortcutToggleDiff);
        Mousetrap.bind(['s'], shortcutToggleSide);
        Mousetrap.bind(['f'], shortcutToggleFull);
        Mousetrap.bind(['r'], shortcutGotoPreviousDiffVersion);
        Mousetrap.bind(['e'], shortcutGotoNextDiffVersion);
    }
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

