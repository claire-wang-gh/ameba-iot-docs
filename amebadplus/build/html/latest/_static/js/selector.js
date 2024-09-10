/* ============= Support Multiple Versions ============= */

function add_selector() {
    return fetch("http://172.29.37.179:88/_static/config.json")
        .then(res => res.json())
        .then(res => {
            var cur_ic = window.location.pathname.split('/')[2];
            var ics = Object.keys(res)
            var versions = res[cur_ic]
            var languages = ["en", "cn"]
            let p = document.getElementById("rtd-search-form").parentElement;
            p.innerHTML = `
            <table>
            <tr>
            <td>IC</td>
            <td>
            <select name="ic" id="ic-selector" title="ic" onchange="change_ic()" style="width:100px; border-radius:2px; margin-bottom:15px">
            ${ics.map(ic => {
                return `<option value="${ic}">${ic}</option>`;
            })}
            </select>
            </td>
            </tr>
            <tr>
            <td>Version</td>
            <td>
            <select name="version" id="version-selector" title="version" onchange="change_version()" style="width:100px; border-radius:2px; margin-bottom:15px">
            ${versions.map(version => {
                return `<option value="${version}">${version}</option>`;
            })}
            </select>
            </td>
            </tr>
            <tr>
            <td>Language</td>
            <td>
            <select name="language" id="language-selector" title="language" onchange="change_language()" style="width:100px; border-radius:2px; margin-bottom:15px">
            ${languages.map(language => {
                return `<option value="${language}">${language}</option>`;
            })}
            </select>
            </td>
            </tr>
            </table>`  + p.innerHTML;
        });
}


/* ============= Toggle IC ============= */
function change_ic() {
    var cur_ic = window.location.pathname.split('/')[2];
    var next_ic = document.getElementById("ic-selector").value;
    window.location.href = location.href.replace("/" + cur_ic + "/", "/" + next_ic + "/");
}
/* ============= Toggle Languages ============= */
function change_language(lang) {
    var cur_language = window.location.pathname.split('/')[3];
    var next_language = document.getElementById("language-selector").value;
    window.location.href = location.href.replace("/" + cur_language + "/", "/" + next_language + "/");
}
/* ============= Toggle Version ============= */
function change_version() {
    var cur_version = window.location.pathname.split('/')[1];
    var next_version = document.getElementById("version-selector").value;
    window.location.href = location.href.replace("/" + cur_version + "/", "/" + next_version + "/");
}

/* ============= Init selector ============= */
document.addEventListener('DOMContentLoaded', (event) => {
    add_selector().then(() => {
        var cur_ic = window.location.pathname.split('/')[2];
        document.getElementById("ic-selector").value = cur_ic;
        var cur_language = window.location.pathname.split('/')[3];
        document.getElementById("language-selector").value = cur_language;
        var cur_version = window.location.pathname.split('/')[1];
        document.getElementById("version-selector").value = cur_version;
    });
})

