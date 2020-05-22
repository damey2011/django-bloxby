const express = require('express');
const mysql = require('mysql');
const bodyparser = require('body-parser');
const fs = require('fs');
const request = require('request');
const app = express();

app.use(bodyparser.json());

let pool = mysql.createPool({
    host: '159.65.79.47',
    user: 'root',
    password: 'dn4F9#Fld49-/#9j',
    database: 'bloxby'
});

const connectSQL = () => {
    return new Promise(res => {
        pool.getConnection((err, connection) => {
            if (err) throw err;
            res(connection)
        })
    })
}

const disconnectSQL = (connection) => {
    connection.release()
}


app.listen('3000', '0.0.0.0', () => {
    console.log('Server is listening at port 3000...')
});

app.get('/:auto_login_token/templates', (req, res) => {
    const sql_query = 'SELECT users_id, sites_id, sites_name, sitethumb, sites_lastupdate_on FROM sites INNER JOIN users ON sites.users_id=users.id WHERE users.auto_login_token=?;'
    connectSQL()
        .then(connection => {
            connection.query(sql_query, [req.params.auto_login_token], (err, rows, fields) => {
                if (!err) {
                    disconnectSQL(connection)
                    res.send(rows)
                } else {
                    disconnectSQL(connection)
                    res.send(err.toString())
                }
            })
        })
})


const signIn = async (email, password) => {
    return new Promise((res, rej) => {
        request.post({
            url: 'http://clouddigitalmarketing.com/auth',
            formData: {'email': email, 'password': password, 'remember': 1},
            followAllRedirects: true
        }, (err, resp, body) => {
            let cookie_str = '';
            resp.headers['set-cookie'].forEach(cookie => {
                cookie_str += cookie.split(';')[0].replace(' ', '')
                cookie_str += '; '
            })
            res(cookie_str)
        })
    })
}

app.get('/:site_id/export', (req, res) => {
    const sql_query = 'SELECT pages_name FROM pages WHERE sites_id=?';
    const fileName = 'website.zip';
    try {
        fs.unlinkSync(fileName);
    } catch (err) {
        console.error(err)
    }
    const file = fs.createWriteStream(fileName);
    connectSQL()
        .then(connection => {
            connection.query(sql_query, [req.params.site_id], (err, rows, fields) => {
                let data = {
                    siteID: req.params.site_id,
                    markup: '',
                    doctype: '<!DOCTYPE html>'
                }
                disconnectSQL(connection)
                rows.forEach(page => {
                    data[`pages[${page.pages_name}]`] = ''
                })

                signIn('exporter@virtualfusions.com', 'Muhammad007').then(async cookies => {
                    if (!cookies.includes('bloxby_login_token')) {
                        res.send({"status": "Login Failed"})
                    } else {
                        let response = await request.post({
                            url: 'http://clouddigitalmarketing.com/sites/export',
                            formData: data,
                            followAllRedirects: true,
                            responseType: 'stream',
                            headers: {
                                'Cookie': cookies,
                            },
                            gzip: true
                        });

                        response.pipe(file);

                        file.on('finish', () => {
                            res.sendFile(fileName, {root: __dirname});
                        });

                        file.on('error', () => {
                            res.send('Error downloading')
                        });
                    }
                })
            })
        })
        .catch(err => {
            res.send('Error getting connection from pool.')
        })
})

