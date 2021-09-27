import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImenicaComponent } from './imenica.component';

describe('ImenicaComponent', () => {
  let component: ImenicaComponent;
  let fixture: ComponentFixture<ImenicaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImenicaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImenicaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
