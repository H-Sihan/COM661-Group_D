import { Injectable } from '@angular/core';
import jsonData from '../data/business.json';

@Injectable({
    providedIn: 'root'
})
export class BusinessData {

    pageSize: number = 3;
    
    getBusinesses(page: number){
        let pageStart = (page - 1) * this.pageSize;
        let pageEnd = pageStart + this.pageSize;
        return jsonData.slice(pageStart, pageEnd);
    }
}
