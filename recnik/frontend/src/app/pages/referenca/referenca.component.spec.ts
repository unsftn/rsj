import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReferencaComponent } from './referenca.component';

describe('ReferencaComponent', () => {
  let component: ReferencaComponent;
  let fixture: ComponentFixture<ReferencaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReferencaComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReferencaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
