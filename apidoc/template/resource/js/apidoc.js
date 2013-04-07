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
    if (element == null) {
        header.hide();
        return;
    }

    element = $(element);
    var elementTop = element.offset().top;
    if (elementTop > scrollTop || elementTop + element.height() - 5 < scrollTop + header.height()) {
        header.hide();
        return;
    }

    if (header.data('element') == element.attr('id')) {
        header.css({
                width: element.width() + 2
            })
            .show();
        return;
    }

    $("H4", header).html(element.find("> H4").html());
    $("> .versions", header).html(element.find("> .versions").html());
    if (element.data("method") !== undefined) {
        header.attr("data-method", element.data("method"));
    } else {
        header.attr("data-method", null);
    }

    header.data("element", element.attr('id'))
        .css({
            width: element.width() + 2
        })
        .show();
}

function initScrollHeader() {
    $(window).on('scroll resize', displayScrollHeader);
}

function displayVersion() {
    $(".method, .type").find(" > .contents > LI").hide();
    if (conf.version == null) {
        $(".method, .type").find(" > .contents > LI:last-child").show();
    } else {
        $("#nav-versions > LI[data-version].active").removeClass("active");
        $("#nav-versions > LI[data-version=\"" + conf.version + "\"]").addClass("active");

        $(".item").find(" > .versions > LI[data-version].active").removeClass("active");
        $(".item").find(" > .versions > LI[data-version=\"" + conf.version + "\"]").addClass("active");

        $(".method, .type").find(" > .versions > LI[data-version~=\"" + conf.version + "\"]").addClass("active");
        $(".method, .type").find(" > .contents > LI[data-version~=\"" + conf.version + "\"]").show();
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
        conf.version = parameters.version;
        displayVersion(parameters.version);
    }

    if (parameters.section) {
        if (parameters.method) {
            $("BODY").scrollTop($("#m-" + parameters.section + "-" + parameters.method).offset().top - conf.scrollMargin);
        } else {
            $("BODY").scrollTop($("#s-" + parameters.section).offset().top - conf.scrollMargin);
        }
    } else if (parameters.namespace) {
        if (parameters.type) {
            $("BODY").scrollTop($("#t-" + parameters.type).offset().top - conf.scrollMargin);
        } else {
            $("BODY").scrollTop($("#n-" + parameters.namespace).offset().top - conf.scrollMargin);
        }
    } else if (parameters.type) {
        $("BODY").scrollTop($("#t-" + parameters.type).offset().top - conf.scrollMargin);
    }
}

function navigateTo(newParameters, removeParameters) {
    var parameters = hashToParameters(window.location.hash);
    if (removeParameters != null) {
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

$(document).ready(function () {
    initScrollNavigation();
    initScrollHeader();
    initNavigation();

    onNavigationChange();
});

