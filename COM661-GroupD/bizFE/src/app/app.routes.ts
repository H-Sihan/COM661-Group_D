import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { Businesses } from './components/businesses/businesses';
import { Business } from './components/businesses/business/business';

// ng g c business
export const routes: Routes = [
    {
        path: '',
        component: Home
    },
    {
        path: 'businesses',
        component: Businesses
    },
    {
        path: 'businesses/:id',
        component: Business
    }
];
