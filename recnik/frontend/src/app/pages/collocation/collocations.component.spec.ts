import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CollocationsComponent } from './collocations.component';

describe('TabFormComponent', () => {
  let component: CollocationsComponent;
  let fixture: ComponentFixture<CollocationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CollocationsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CollocationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
