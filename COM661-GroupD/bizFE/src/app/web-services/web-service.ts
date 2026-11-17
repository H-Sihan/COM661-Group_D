import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class WebService {
    pageSize: number = 3;

    constructor(private http: HttpClient) {}

    getBusinesses(page: number){
        return this.http.get<any>(
            'http://127.0.0.1:5001/api/v1.0/businesses?pn=' + 
            page + '&ps=' + this.pageSize);
    }
}
