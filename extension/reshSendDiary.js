const reshSendDiary = async ()=>{
  if(location.hostname == 'resh.edu.ru' && document.querySelector("body > div.outer-sf > div > header > div > div > div.d-tc.header-top__login-cell > div > a:nth-child(1)")== null){
    const res = (await (await fetch('https://resh.edu.ru/office/user/diary/', {credentials: 'include'})).text())
    const parser = new DOMParser();
    const table = parser.parseFromString(res, "text/html").getElementsByTagName('table')[0];
    const trs = table.getElementsByTagName('tr');
    const parsed = [];
    for (let index = 0; index < trs.length; index++) {
        const e = trs[index];
        if(index!=0){
            const tds = e.getElementsByTagName('p');
            if(tds.length >0){
                parsed.push(`${tds[1].innerText} @ ${tds[2].innerText.trim()} | ${tds[4].innerText.trim()} | ${tds[5].innerText.trim()}`);
            }
        }
    }

    await fetch('https://ДОМЕН:8808/update', {method: 'post', headers: {'Content-Type': 'application/json','Authorization': 'Bearer token'}, body:JSON.stringify({'data': JSON.stringify(parsed)})});
  }
};
setInterval(reshSendDiary,60000);
reshSendDiary();