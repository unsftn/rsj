import { NgModule } from '@angular/core';
import { FieldsetModule } from 'primeng/fieldset';
import { HomeComponent } from './home.component';

@NgModule({
    declarations: [HomeComponent],
    imports: [FieldsetModule],
    exports: [HomeComponent],
    providers: [],
    bootstrap: [HomeComponent],
})
export class HomeModule {}
