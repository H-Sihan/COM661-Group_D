import { Component } from '@angular/core';
import { BusinessData } from '../../services/business-data';
import { RouterLink } from '@angular/router';
import { RouterOutlet, RouterModule } from '@angular/router';
import { WebService } from '../../web-services/web-service';

@Component({
  imports: [RouterLink, RouterOutlet, RouterModule],
  providers: [BusinessData, WebService],
  selector: 'app-businesses',
  styleUrl: './businesses.css',
  templateUrl: './businesses.html',
})
export class Businesses {

  business_list: any = [ ];
  page: number = 1;

  constructor(private businessData: BusinessData,
              private webService: WebService) { }

  ngOnInit() {
    //this.business_list = this.businessData.getBusinesses(this.page);
    this.webService.getBusinesses(this.page).subscribe(
      (response) => {
        this.business_list = response;
      }
    )
  }

  nextPage(){
    if (this.page < this.businessData.getLastPageNumber()){
      this.page = this.page + 1
      //this.business_list = this.businessData.getBusinesses(this.page);
      this.webService.getBusinesses(this.page).subscribe(
        (response) => {
          this.business_list = response;
        }
      )
    }
  }
  previousPage() {
    if(this.page > 1){
      this.page = this.page - 1
      //this.business_list = this.businessData.getBusinesses(this.page);
      this.webService.getBusinesses(this.page).subscribe(
        (response) => {
          this.business_list = response;
        }
      )
    }
  }
}
